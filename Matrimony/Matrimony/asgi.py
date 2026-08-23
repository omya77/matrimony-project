import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Matrimony.settings')
django_asgi_app = get_asgi_application()

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='misalomkar555@gmail.com').exists():
        User.objects.create_superuser('misalomkar555@gmail.com', 'misalomkar555@gmail.com', 'Omkar@1234')
except Exception:
    pass

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import interactions_app.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            interactions_app.routing.websocket_urlpatterns
        )
    ),
})
