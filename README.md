# Atelier Aura — Django

Full Django web application migrated from static HTML.

## Features

- **Home page** — hero, services, pricing preview, CTA
- **Plans page** — live pricing plans from DB with Add to Cart
- **Shopping cart** — session-based for guests, user-linked for logged-in
- **Checkout** — order summary + demo payment form
- **Order confirmation** — order success page with reference number
- **User auth** — register, login, logout, dashboard with order history
- **Contact form** — full Django backend, saves to DB, emails admin
- **Newsletter** — email subscriptions stored in DB (replaces Google Script)
- **Admin panel** — manage plans, features, orders, contacts, subscribers

## Quick Start

```bash
bash start.sh
```

Then visit http://127.0.0.1:8000

## Admin Credentials

- URL: http://127.0.0.1:8000/admin/
- Username: `admin`
- Password: `Admin@2026!`

## Structure

```
atelierAura/
├── atelierAura/      # Django project config
├── core/             # Home, contact, newsletter
├── accounts/         # Auth: register, login, dashboard
├── shop/             # Plans, cart, checkout, orders
├── templates/        # Base + per-app templates
├── seed_data.py      # Seeds 3 default plans
├── start.sh          # One-command startup
└── db.sqlite3        # SQLite database
```

## Running Tests

```bash
python manage.py test
```

32 tests across all 3 apps.

## Stripe Integration

Replace placeholder keys in `settings.py`:

```python
STRIPE_PUBLIC_KEY = 'pk_live_...'
STRIPE_SECRET_KEY = 'sk_live_...'
```

## Email in Production

Change `EMAIL_BACKEND` in `settings.py` to SMTP:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yourprovider.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your@email.com'
EMAIL_HOST_PASSWORD = 'yourpassword'
```
