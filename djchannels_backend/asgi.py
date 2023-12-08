import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chatapp.middleware import JWTAuthMiddleware

import chap_2.routing
import chap_3.routing
import chatapp.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djchannels_backend.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            JWTAuthMiddleware(
                URLRouter(
                    chap_2.routing.websocket_urlpatterns
                    + chap_3.routing.websocket_urlpatterns
                    + chatapp.routing.websocket_urlpatterns
                )
            )
        ),
    }
)
