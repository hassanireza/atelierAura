from .models import Cart


def cart_count(request):
    count = 0
    try:
        cart = _get_cart(request)
        if cart:
            count = cart.get_item_count()
    except Exception:
        pass
    return {'cart_count': count}


def _get_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if not session_key:
            return None
        cart = Cart.objects.filter(session_key=session_key, user=None).first()
    return cart
