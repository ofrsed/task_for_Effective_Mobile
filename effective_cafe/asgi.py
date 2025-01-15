import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from business_logic.routing import websocket_urlpatterns  # Подключаем маршруты из приложения

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'effective_cafe.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Используем правильные маршруты WebSocket
        )
    ),
})