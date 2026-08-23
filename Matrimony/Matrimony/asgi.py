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

# Auto-seed database on Render
try:
    if os.environ.get('RENDER'):
        from profiles_app.models import Religion, Caste, MotherTongue
        religions_castes = {
            "Hindu": ["Brahmin", "Maratha", "Rajput", "Baniya", "Yadav", "Kunbi", "Kayastha", "Lingayat", "Other"],
            "Muslim": ["Sunni", "Shia", "Pathan", "Syed", "Sheikh", "Other"],
            "Christian": ["Catholic", "Protestant", "Orthodox", "Other"],
            "Sikh": ["Jat", "Khatri", "Arora", "Ramgarhia", "Other"],
            "Jain": ["Digambar", "Shwetambar", "Other"],
            "Buddhist": ["Navayana", "Mahayana", "Other"],
            "Parsi": ["Parsi", "Irani"]
        }
        for rel_name, castes in religions_castes.items():
            religion, _ = Religion.objects.get_or_create(name=rel_name, defaults={'is_active': True})
            for caste_name in castes:
                Caste.objects.get_or_create(religion=religion, name=caste_name, defaults={'is_active': True})
        
        languages = ["Hindi", "Marathi", "English", "Bengali", "Telugu", "Tamil", "Gujarati", "Urdu", "Kannada", "Odia", "Malayalam", "Punjabi", "Assamese", "Maithili", "Other"]
        for lang in languages:
            MotherTongue.objects.get_or_create(name=lang, defaults={'is_active': True})
            
        from payments_app.models import MembershipPlan
        plans = [
            ("Basic", 999.00, 1, "Send 50 interests/day\nView verified profiles\nBasic Support"),
            ("Premium", 1999.00, 3, "Send unlimited interests\nView direct contact details\nPriority Support\nProfile Highlighting"),
            ("Elite", 3999.00, 6, "All Premium Features\nDedicated Relationship Manager\nBackground Verification\nTop Search Ranking")
        ]
        for name, price, dur, feat in plans:
            MembershipPlan.objects.get_or_create(name=name, defaults={'price': price, 'duration_months': dur, 'features': feat, 'is_active': True})
except Exception:
    pass
