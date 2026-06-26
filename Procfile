web: python manage.py migrate --run-syncdb && python manage.py collectstatic --noinput && python seed_data.py && gunicorn atelierAura.wsgi --bind 0.0.0.0:$PORT

