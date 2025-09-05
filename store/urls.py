from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),

    # Catalog & Product
    path('category/<slug:slug>/', views.product_list, name='product_list_by_category'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:medicine_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),

    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('my/orders/', views.my_orders, name='my_orders'),

    # Profile & Address
    path('profile/', views.profile, name='profile'),
    path('address/add/', views.add_address, name='add_address'),
    path('address/<int:address_id>/make-default/', views.make_default_address, name='make_default_address'),

    # Admin (custom lightweight dashboard)
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/medicines/', views.admin_medicine_list, name='admin_medicine_list'),
    path('dashboard/medicines/add/', views.admin_medicine_create, name='admin_medicine_create'),
    path('dashboard/medicines/<int:pk>/edit/', views.admin_medicine_update, name='admin_medicine_update'),
    path('dashboard/medicines/<int:pk>/delete/', views.admin_medicine_delete, name='admin_medicine_delete'),

    path('dashboard/orders/', views.admin_orders, name='admin_orders'),
    path('dashboard/orders/<int:pk>/status/', views.admin_order_status, name='admin_order_status'),
]