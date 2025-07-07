import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from appschedule import routing as schedule_routing # OAHP
from channels.auth import AuthMiddlewareStack  # OAHP
from django.urls import re_path
from appschedule.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            schedule_routing.websocket_urlpatterns
        )
    ),
})