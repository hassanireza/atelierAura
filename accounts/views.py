from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db import transaction

from .forms import RegisterForm, LoginForm
from .models import UserProfile


def auth_view(request):
    """Unified login/register page with tab switching."""
    if request.user.is_authenticated:
        return redirect('home')

    # Determine which tab is active
    active_tab = request.GET.get('tab', 'login')

    login_form = LoginForm()
    register_form = RegisterForm()

    if request.method == 'POST':
        action = request.POST.get('action', 'login')

        if action == 'login':
            active_tab = 'login'
            login_form = LoginForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)

        elif action == 'register':
            active_tab = 'register'
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                with transaction.atomic():
                    user = register_form.save()
                    UserProfile.objects.create(user=user)
                login(request, user)
                messages.success(request, f'Welcome to Atelier Aura, {user.first_name or user.username}!')
                next_url = request.GET.get('next', '/')
                return redirect(next_url)

    return render(request, 'accounts/auth.html', {
        'login_form': login_form,
        'register_form': register_form,
        'active_tab': active_tab,
    })


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    from shop.models import Order
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/dashboard.html', {'orders': orders})
