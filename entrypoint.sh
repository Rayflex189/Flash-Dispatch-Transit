#!/bin/sh
set -e

echo "======================================"
echo "FLASH DISPATCH STARTUP"
echo "======================================"

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Checking administrator account..."

python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if not all([username, email, password]):
    print("ERROR: Administrator environment variables are missing.")
else:
    user = User.objects.filter(username=username).first()

    if user:
        print(f"Administrator '{username}' already exists.")
    else:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        print(f"SUCCESS: Administrator '{username}' created.")
PY

echo "Starting Gunicorn..."

exec gunicorn flash_dispatch.wsgi:application \
    --bind 0.0.0.0:8020 \
    --workers 2 \
    --worker-class sync
