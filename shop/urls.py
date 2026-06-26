from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.plans, name='plans'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:plan_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/place-order/', views.place_order, name='place_order'),
    path('order/<uuid:order_id>/success/', views.order_success, name='order_success'),
]
