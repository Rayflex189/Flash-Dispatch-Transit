"""
WSGI config for flash_dispatch project.
This is the traditional synchronous server interface.
"""

import os
import sys

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flash_dispatch.settings')

# Standard WSGI application for traditional servers (Gunicorn, uWSGI, Apache)
application = get_wsgi_application()

# For development server
app = application