import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Matrimony.settings')
django_asgi_app = get_asgi_application()

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='misalomkar555@gmail.com').exists():
        User.objects.create_superuser('misalomkar555@gmail.com', 'misalomkar555@gmail.com', 'Omkar@1234')
        from django.contrib.auth.models import User
        from profiles_app.models import Profile
        from datetime import date
        import random
        if Profile.objects.count() < 10:
            first_names_m = ['Aarav', 'Vihaan', 'Aditya', 'Rohan', 'Kabir', 'Aryan', 'Dhruv', 'Ishaan', 'Karan', 'Rahul']
            first_names_f = ['Aanya', 'Diya', 'Sanya', 'Priya', 'Kavya', 'Riya', 'Ananya', 'Myra', 'Sneha', 'Neha']
            last_names = ['Sharma', 'Patil', 'Deshmukh', 'Singh', 'Gupta', 'Khan', 'Syed', 'Thomas', 'Kaur', 'Gill']
            cities = ['Mumbai', 'Pune', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Ahmedabad']
            for rel, castes in religions_castes.items():
                for caste in castes:
                    for gender in ['Male', 'Female']:
                        for i in range(2):
                            is_male = gender == 'Male'
                            fname = random.choice(first_names_m) if is_male else random.choice(first_names_f)
                            lname = random.choice(last_names)
                            username = f'{fname.lower()}_{caste.lower()}_{random.randint(100,999)}'
                            user, created = User.objects.get_or_create(username=username, defaults={'email': f'{username}@example.com'})
                            if created:
                                user.set_password('password123')
                                user.save()
                                Profile.objects.create(user=user, full_name=f'{fname} {lname}', gender=gender, dob=date(1995, 1, 1), religion=rel, caste=caste, city=random.choice(cities), is_photo_approved=True)
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
        from django.contrib.auth.models import User
        from profiles_app.models import Profile
        from datetime import date
        import random
        if Profile.objects.count() < 10:
            first_names_m = ['Aarav', 'Vihaan', 'Aditya', 'Rohan', 'Kabir', 'Aryan', 'Dhruv', 'Ishaan', 'Karan', 'Rahul']
            first_names_f = ['Aanya', 'Diya', 'Sanya', 'Priya', 'Kavya', 'Riya', 'Ananya', 'Myra', 'Sneha', 'Neha']
            last_names = ['Sharma', 'Patil', 'Deshmukh', 'Singh', 'Gupta', 'Khan', 'Syed', 'Thomas', 'Kaur', 'Gill']
            cities = ['Mumbai', 'Pune', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Ahmedabad']
            for rel, castes in religions_castes.items():
                for caste in castes:
                    for gender in ['Male', 'Female']:
                        for i in range(2):
                            is_male = gender == 'Male'
                            fname = random.choice(first_names_m) if is_male else random.choice(first_names_f)
                            lname = random.choice(last_names)
                            username = f'{fname.lower()}_{caste.lower()}_{random.randint(100,999)}'
                            user, created = User.objects.get_or_create(username=username, defaults={'email': f'{username}@example.com'})
                            if created:
                                user.set_password('password123')
                                user.save()
                                Profile.objects.create(user=user, full_name=f'{fname} {lname}', gender=gender, dob=date(1995, 1, 1), religion=rel, caste=caste, city=random.choice(cities), is_photo_approved=True)
except Exception:
    pass
