#!/bin/bash
# Atelier Aura — Django startup script
set -e

echo "=== Atelier Aura ==="
cd "$(dirname "$0")"

echo "[1/4] Installing dependencies..."
pip install django pillow stripe --break-system-packages -q

echo "[2/4] Applying migrations..."
python manage.py migrate --run-syncdb

echo "[3/4] Collecting static files..."
python manage.py collectstatic --noinput

echo "[4/4] Seeding default plans (if empty)..."
python seed_data.py

echo ""
echo "✓ Ready! Starting server at http://127.0.0.1:8000"
echo "  Admin panel: http://127.0.0.1:8000/admin/"
echo "  Admin login: admin / Admin@2026!"
echo ""
python manage.py runserver 0.0.0.0:8000
