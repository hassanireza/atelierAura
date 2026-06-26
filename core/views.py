from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
import json

from .models import ContactMessage, NewsletterSubscriber


def home(request):
    return render(request, 'core/home.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        msg = request.POST.get('message', '').strip()
        if not name or not email or not msg:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'All fields are required.'})
            messages.error(request, 'All fields are required.')
            return render(request, 'core/contact.html', {'name': name, 'email': email, 'message': msg})
        ContactMessage.objects.create(name=name, email=email, message=msg)
        try:
            send_mail(
                subject=f'New contact from {name}',
                message=f'Name: {name}\nEmail: {email}\n\nMessage:\n{msg}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        messages.success(request, "Your message has been sent. We'll be in touch soon!")
        return redirect('contact')
    return render(request, 'core/contact.html')


@require_POST
def newsletter_subscribe(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
    except (json.JSONDecodeError, AttributeError):
        email = request.POST.get('email', '').strip()
    if not email:
        return JsonResponse({'success': False, 'error': 'Email is required.'})
    obj, created = NewsletterSubscriber.objects.get_or_create(email=email)
    if not created:
        obj.is_active = True
        obj.save()
        return JsonResponse({'success': True, 'message': "You're already subscribed!"})
    return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'})


def service_web_design(request):
    return render(request, 'core/service_web_design.html')


def service_frontend(request):
    return render(request, 'core/service_frontend.html')


def service_seo(request):
    return render(request, 'core/service_seo.html')


def about(request):
    return render(request, 'core/about.html')


def faq(request):
    return render(request, 'core/faq.html')
