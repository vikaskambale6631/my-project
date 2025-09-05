from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q, F
from .models import Category, Medicine, Cart, CartItem, Address, Order, OrderItem, Prescription
from .forms import SignUpForm, AddressForm, MedicineForm, PrescriptionForm

def is_staff(user):
    return user.is_staff

# ---------- Public & User Module ----------

def home(request):
    categories = Category.objects.all().order_by('name')
    medicines = Medicine.objects.order_by('-created_at')[:8]
    q = request.GET.get('q')
    if q:
        medicines = Medicine.objects.filter(
            Q(name__icontains=q) | Q(brand__icontains=q) | Q(description__icontains=q)
        )
    return render(request, 'store/home.html', {'categories': categories, 'medicines': medicines})

def product_list(request, slug=None):
    category = None
    categories = Category.objects.all().order_by('name')
    medicines = Medicine.objects.all()
    q = request.GET.get('q')
    if slug:
        category = get_object_or_404(Category, slug=slug)
        medicines = medicines.filter(category=category)
    if q:
        medicines = medicines.filter(Q(name__icontains=q) | Q(brand__icontains=q) | Q(description__icontains=q))
    return render(request, 'store/product_list.html', {'categories': categories, 'category': category, 'medicines': medicines})

def product_detail(request, slug):
    product = get_object_or_404(Medicine, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})

def _get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart

@login_required
def add_to_cart(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    cart = _get_or_create_cart(request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, medicine=medicine)
    if not created:
        item.quantity = F('quantity') + 1
        item.save()
        item.refresh_from_db()
    messages.success(request, f"Added {medicine.name} to cart.")
    return redirect('cart')

@login_required
def cart_view(request):
    cart = _get_or_create_cart(request.user)
    items = cart.items.select_related('medicine')
    need_rx = any(i.medicine.rx_required for i in items)
    return render(request, 'store/cart.html', {'cart': cart, 'items': items, 'need_rx': need_rx})

@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    qty = int(request.POST.get('quantity', 1))
    if qty <= 0:
        item.delete()
    else:
        item.quantity = qty
        item.save()
    return redirect('cart')

@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart')

@login_required
def checkout(request):
    cart = _get_or_create_cart(request.user)
    items = cart.items.select_related('medicine')
    if not items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('product_list')

    need_rx = any(i.medicine.rx_required for i in items)

    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        address = get_object_or_404(Address, id=address_id, user=request.user)

        # Fake payment -> COD / simulate success
        order = Order.objects.create(user=request.user, address=address, payment_status='cod', order_status='placed')
        total = 0
        for i in items:
            price = i.medicine.price
            OrderItem.objects.create(order=order, medicine=i.medicine, quantity=i.quantity, price=price)
            i.medicine.stock = max(0, i.medicine.stock - i.quantity)
            i.medicine.save()
            total += float(price) * i.quantity
        order.total_amount = total
        order.save()

        # Handle prescription upload if required
        if need_rx and request.FILES.get('file'):
            form = PrescriptionForm(request.POST, request.FILES)
            if form.is_valid():
                pres = form.save(commit=False)
                pres.user = request.user
                pres.order = order
                pres.save()
        # Clear cart
        cart.items.all().delete()
        return redirect('order_success', order_id=order.id)

    addresses = request.user.addresses.all().order_by('-is_default', '-created_at')
    pres_form = PrescriptionForm()
    return render(request, 'store/checkout.html', {'cart': cart, 'items': items, 'addresses': addresses, 'need_rx': need_rx, 'pres_form': pres_form})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_success.html', {'order': order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/orders.html', {'orders': orders})

@login_required
def profile(request):
    addresses = request.user.addresses.all().order_by('-is_default', '-created_at')
    form = AddressForm()
    return render(request, 'store/profile.html', {'addresses': addresses, 'form': form})

@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            addr = form.save(commit=False)
            addr.user = request.user
            if addr.is_default:
                Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
            addr.save()
    return redirect('profile')

@login_required
def make_default_address(request, address_id):
    addr = get_object_or_404(Address, id=address_id, user=request.user)
    Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
    addr.is_default = True
    addr.save()
    return redirect('profile')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Cart.objects.get_or_create(user=user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'store/signup.html', {'form': form})

# ---------- Admin Module (Custom) ----------

@user_passes_test(is_staff)
def admin_dashboard(request):
    stats = {
        'users': request.user.__class__.objects.count(),
        'products': Medicine.objects.count(),
        'orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(order_status='placed').count()
    }
    return render(request, 'store/admin_dashboard.html', stats)

@user_passes_test(is_staff)
def admin_medicine_list(request):
    q = request.GET.get('q')
    meds = Medicine.objects.all().order_by('-created_at')
    if q:
        meds = meds.filter(Q(name__icontains=q) | Q(brand__icontains=q))
    return render(request, 'store/admin_medicine_list.html', {'medicines': meds})

@user_passes_test(is_staff)
def admin_medicine_create(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Medicine added.")
            return redirect('admin_medicine_list')
    else:
        form = MedicineForm()
    return render(request, 'store/admin_medicine_form.html', {'form': form, 'title': 'Add Medicine'})

@user_passes_test(is_staff)
def admin_medicine_update(request, pk):
    med = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES, instance=med)
        if form.is_valid():
            form.save()
            messages.success(request, "Medicine updated.")
            return redirect('admin_medicine_list')
    else:
        form = MedicineForm(instance=med)
    return render(request, 'store/admin_medicine_form.html', {'form': form, 'title': 'Edit Medicine'})

@user_passes_test(is_staff)
def admin_medicine_delete(request, pk):
    med = get_object_or_404(Medicine, pk=pk)
    med.delete()
    messages.success(request, "Medicine deleted.")
    return redirect('admin_medicine_list')

@user_passes_test(is_staff)
def admin_orders(request):
    orders = Order.objects.select_related('user').order_by('-created_at')
    return render(request, 'store/admin_orders.html', {'orders': orders})

@user_passes_test(is_staff)
def admin_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    status = request.POST.get('order_status')
    if status in dict(Order.ORDER_STATUS_CHOICES):
        order.order_status = status
        order.save()
        messages.success(request, "Order status updated.")
    return redirect('admin_orders')