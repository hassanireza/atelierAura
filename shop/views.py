from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Plan, Cart, CartItem, Order, OrderItem


def _get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user, defaults={'session_key': ''})
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
    return cart


def _get_cart(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).first()
    session_key = request.session.session_key
    if not session_key:
        return None
    return Cart.objects.filter(session_key=session_key, user=None).first()


def plans(request):
    all_plans = Plan.objects.filter(is_active=True).prefetch_related('features')
    return render(request, 'shop/plans.html', {'plans': all_plans})


@require_POST
def add_to_cart(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id, is_active=True)
    cart = _get_or_create_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, plan=plan)
    if not created:
        item.quantity += 1
        item.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_count': cart.get_item_count(), 'message': f'{plan.name} added to cart!'})
    messages.success(request, f'{plan.name} added to cart!')
    return redirect('cart')


def cart_view(request):
    cart = _get_cart(request)
    items = cart.items.select_related('plan').all() if cart else []
    total = cart.get_total() if cart else 0
    return render(request, 'shop/cart.html', {'cart': cart, 'items': items, 'total': total})


@require_POST
def remove_from_cart(request, item_id):
    cart = _get_cart(request)
    if cart:
        CartItem.objects.filter(id=item_id, cart=cart).delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = _get_cart(request)
        return JsonResponse({'success': True, 'cart_count': cart.get_item_count() if cart else 0, 'total': str(cart.get_total()) if cart else '0.00'})
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')


@require_POST
def update_cart(request, item_id):
    cart = _get_cart(request)
    qty = int(request.POST.get('quantity', 1))
    if cart:
        item = CartItem.objects.filter(id=item_id, cart=cart).first()
        if item:
            if qty < 1:
                item.delete()
            else:
                item.quantity = qty
                item.save()
    return redirect('cart')


@login_required
def checkout(request):
    cart = _get_cart(request)
    if not cart or not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('plans')
    total = cart.get_total()
    return render(request, 'shop/checkout.html', {
        'cart': cart,
        'items': cart.items.select_related('plan').all(),
        'total': total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })


@login_required
@require_POST
def place_order(request):
    cart = _get_cart(request)
    if not cart or not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('plans')

    # Validate payment fields
    card_number = request.POST.get('card_number', '').replace(' ', '')
    expiry = request.POST.get('expiry', '').strip()
    cvc = request.POST.get('cvc', '').strip()

    errors = []
    if len(card_number) < 16:
        errors.append('Please enter a valid 16-digit card number.')
    if len(expiry) < 4:
        errors.append('Please enter a valid expiry date (MM/YY).')
    if len(cvc) < 3:
        errors.append('Please enter a valid CVC.')

    if errors:
        for e in errors:
            messages.error(request, e)
        return redirect('checkout')

    total = cart.get_total()
    order = Order.objects.create(
        user=request.user,
        total=total,
        status='paid',
        stripe_payment_intent='demo_' + str(Order.objects.count() + 1),
    )
    for item in cart.items.select_related('plan').all():
        OrderItem.objects.create(
            order=order, plan=item.plan, plan_name=item.plan.name,
            price=item.plan.price, quantity=item.quantity,
        )
    cart.items.all().delete()
    messages.success(request, f'Order confirmed! Reference: #{str(order.order_id)[:8].upper()}')
    return redirect('order_success', order_id=order.order_id)


def order_success(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'shop/order_success.html', {'order': order})
