#!/bin/sh
set -e

echo "🚀 Starting Flash Dispatch..."

echo "📦 Running migrations..."
python manage.py migrate --noinput

echo "👤 Checking superuser..."

python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if username and email and password:
    user = User.objects.filter(username=username).first()

    if user:
        print(f"✅ Superuser '{username}' already exists.")
    else:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superuser '{username}' created.")
else:
    print("⚠️ Superuser environment variables are not configured.")
PY

echo "🌐 Starting Gunicorn..."

exec gunicorn flash_dispatch.wsgi:application \
    --bind 0.0.0.0:8020 \
    --workers 2 \
    --worker-class sync
