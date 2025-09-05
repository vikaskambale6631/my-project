from django.contrib import admin
from .models import Category, Medicine, Address, Cart, CartItem, Order, OrderItem, Prescription

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'price', 'stock', 'rx_required', 'category')
    list_filter = ('rx_required', 'category')
    search_fields = ('name', 'brand', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'line1', 'city', 'state', 'pincode', 'is_default')
    list_filter = ('city', 'state')
    search_fields = ('line1', 'city', 'state', 'pincode')

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'updated_at')
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'payment_status', 'order_status', 'created_at')
    list_filter = ('payment_status', 'order_status', 'created_at')
    search_fields = ('id', 'user__username')
    inlines = [OrderItemInline]

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order', 'created_at')
    search_fields = ('user__username',)