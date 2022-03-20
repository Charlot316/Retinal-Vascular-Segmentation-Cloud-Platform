"""
ASGI config for eyes project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
# Import other Channels classes and consumers here.
from channels.routing import ProtocolTypeRouter, URLRouter
# from apps.websocket_app.urls import websocket_urlpatterns
from eyes.urls import websocket_urlpatterns
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eyes.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    # Explicitly set 'http' key using Django's ASGI application.
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})