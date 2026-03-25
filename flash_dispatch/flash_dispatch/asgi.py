"""
ASGI config for flash_dispatch project.
This is the asynchronous server interface for WebSockets, HTTP/2, etc.
"""

import os
import sys
from django.core.asgi import get_asgi_application

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flash_dispatch.settings')

# Standard ASGI application for async servers (Daphne, Uvicorn)
django_asgi_app = get_asgi_application()

# You can add WebSocket/Channels here if needed
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import apps.websocket.routing

# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             apps.websocket.routing.websocket_urlpatterns
#         )
#     ),
# })

# For basic ASGI without WebSockets
application = django_asgi_app