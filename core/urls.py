from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('services/website-design/', views.service_web_design, name='service_web_design'),
    path('services/frontend-development/', views.service_frontend, name='service_frontend'),
    path('services/seo-optimization/', views.service_seo, name='service_seo'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
]
