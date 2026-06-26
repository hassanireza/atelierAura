import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atelierAura.settings')
django.setup()

from shop.models import Plan, PlanFeature

Plan.objects.all().delete()

starter = Plan.objects.create(
    name='Starter', slug='starter', plan_type='starter', price=799,
    description='Perfect for small businesses and solo projects.', is_featured=False, order=1
)
for i, f in enumerate(['Single Page Website', 'Responsive Design', 'Basic SEO Setup', 'Fast Delivery (7 days)', 'Contact Form Integration']):
    PlanFeature.objects.create(plan=starter, text=f, order=i)

business = Plan.objects.create(
    name='Business', slug='business', plan_type='business', price=1999,
    description='Ideal for growing businesses needing a full web presence.', is_featured=True, order=2
)
for i, f in enumerate(['Up to 8 Pages', 'Advanced UI Design', 'SEO Optimization', 'Performance Optimization', 'CMS Integration', 'Analytics Setup']):
    PlanFeature.objects.create(plan=business, text=f, order=i)

premium = Plan.objects.create(
    name='Premium', slug='premium', plan_type='premium', price=3999,
    description='Full-service solution for ambitious brands.', is_featured=False, order=3
)
for i, f in enumerate(['Custom Web Experience', 'Animations & Interactions', 'Priority Support (24h)', 'Full SEO & Performance Optimization', 'E-commerce Ready', 'Dedicated Account Manager']):
    PlanFeature.objects.create(plan=premium, text=f, order=i)

print(f"Created {Plan.objects.count()} plans with features.")
