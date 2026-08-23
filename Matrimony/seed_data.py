import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Matrimony.settings')
django.setup()

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

languages = [
    "Hindi", "Marathi", "English", "Bengali", "Telugu", "Tamil", 
    "Gujarati", "Urdu", "Kannada", "Odia", "Malayalam", "Punjabi", 
    "Assamese", "Maithili", "Other"
]

print("Seeding Religions and Castes...")
for rel_name, castes in religions_castes.items():
    religion, created = Religion.objects.get_or_create(name=rel_name, is_active=True)
    for caste_name in castes:
        Caste.objects.get_or_create(religion=religion, name=caste_name, is_active=True)

print("Seeding Mother Tongues...")
for lang in languages:
    MotherTongue.objects.get_or_create(name=lang, is_active=True)

print("Database seeded successfully!")
print(f"Total Religions: {Religion.objects.count()}")
print(f"Total Castes: {Caste.objects.count()}")
print(f"Total Mother Tongues: {MotherTongue.objects.count()}")
