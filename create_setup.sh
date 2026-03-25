#!/bin/bash

echo "🚀 Setting up Flash Dispatch project..."

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p flash_dispatch/apps/{accounts,tracking,dashboard,landing,api}
mkdir -p flash_dispatch/templates/{landing,accounts,tracking,dashboard}
mkdir -p flash_dispatch/static/{css,js,images}
mkdir -p flash_dispatch/media/profiles
mkdir -p flash_dispatch/flash_dispatch

# Create Python package files
echo "📝 Creating Python package files..."
touch flash_dispatch/apps/accounts/__init__.py
touch flash_dispatch/apps/tracking/__init__.py
touch flash_dispatch/apps/dashboard/__init__.py
touch flash_dispatch/apps/landing/__init__.py
touch flash_dispatch/apps/api/__init__.py
touch flash_dispatch/flash_dispatch/__init__.py

# Create main Django files
echo "📝 Creating main Django files..."
touch flash_dispatch/manage.py
touch flash_dispatch/requirements.txt
touch flash_dispatch/flash_dispatch/settings.py
touch flash_dispatch/flash_dispatch/urls.py
touch flash_dispatch/flash_dispatch/wsgi.py

# Create app files
echo "📝 Creating app files..."
# Accounts app
touch flash_dispatch/apps/accounts/apps.py
touch flash_dispatch/apps/accounts/models.py
touch flash_dispatch/apps/accounts/views.py
touch flash_dispatch/apps/accounts/urls.py
touch flash_dispatch/apps/accounts/forms.py
touch flash_dispatch/apps/accounts/admin.py

# Tracking app
touch flash_dispatch/apps/tracking/apps.py
touch flash_dispatch/apps/tracking/models.py
touch flash_dispatch/apps/tracking/views.py
touch flash_dispatch/apps/tracking/urls.py
touch flash_dispatch/apps/tracking/forms.py
touch flash_dispatch/apps/tracking/admin.py

# Dashboard app
touch flash_dispatch/apps/dashboard/apps.py
touch flash_dispatch/apps/dashboard/views.py
touch flash_dispatch/apps/dashboard/urls.py
touch flash_dispatch/apps/dashboard/models.py

# Landing app
touch flash_dispatch/apps/landing/apps.py
touch flash_dispatch/apps/landing/views.py
touch flash_dispatch/apps/landing/urls.py

# API app
touch flash_dispatch/apps/api/apps.py
touch flash_dispatch/apps/api/views.py
touch flash_dispatch/apps/api/urls.py

# Create templates
echo "📝 Creating template files..."
touch flash_dispatch/templates/base.html
touch flash_dispatch/templates/landing/home.html
touch flash_dispatch/templates/accounts/login.html
touch flash_dispatch/templates/accounts/register.html
touch flash_dispatch/templates/accounts/profile.html
touch flash_dispatch/templates/dashboard/home.html
touch flash_dispatch/templates/dashboard/create_shipment.html
touch flash_dispatch/templates/dashboard/shipment_detail.html
touch flash_dispatch/templates/tracking/track.html

# Create static files
echo "📝 Creating static files..."
touch flash_dispatch/static/css/style.css
touch flash_dispatch/static/js/main.js

echo "✅ Project structure created successfully!"
echo ""
echo "Next steps:"
echo "1. cd flash_dispatch"
echo "2. Copy the code from the previous response into the respective files"
echo "3. Run: python -m venv venv"
echo "4. Run: source venv/bin/activate (or venv\Scripts\activate on Windows)"
echo "5. Run: pip install -r requirements.txt"
echo "6. Run: python manage.py migrate"
echo "7. Run: python manage.py createsuperuser"
echo "8. Run: python manage.py runserver"