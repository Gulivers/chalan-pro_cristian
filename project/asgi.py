import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import appschedule.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chalan_pro.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            appschedule.routing.websocket_urlpatterns
        )
    ),
})
