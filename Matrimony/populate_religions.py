import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Matrimony.settings')
django.setup()

from profiles_app.models import Religion, Caste

religions_data = {
    'Hindu': ['Brahmin', 'Maratha', 'Rajput', 'Baniya', 'Kayastha', 'Yadav', 'Kurmi', 'Lingayat', 'Reddy', 'Nair', 'Ezhava', 'Vanniyar', 'Kamma', 'Gowda', 'Chettiar', 'Gounder', 'Nadars', 'Scheduled Caste (SC)', 'Scheduled Tribe (ST)', 'Other Backward Class (OBC)', 'Kunbi', 'Mali'],
    'Muslim': ['Sunni', 'Shia', 'Pathan', 'Syed', 'Sheikh', 'Ansari', 'Memon', 'Bohra'],
    'Christian': ['Catholic', 'Protestant', 'Orthodox', 'Methodist', 'Baptist', 'Marthoma', 'Syrian Catholic'],
    'Sikh': ['Jat', 'Khatri', 'Ramgharia', 'Ahluwalia', 'Arora', 'Rajput', 'Saini'],
    'Jain': ['Digambar', 'Shwetambar', 'Bania', 'Oswal', 'Porwal', 'Khandelwal'],
    'Buddhist': ['Mahayana', 'Theravada', 'Vajrayana', 'Navayana'],
    'Parsi': ['Irani', 'Parsi'],
    'Jewish': ['Orthodox', 'Conservative', 'Reform'],
    'Spiritual': ['Doesn\'t Matter'],
    'Other': ['Doesn\'t Matter']
}

added_religions = 0
added_castes = 0

for rel_name, castes in religions_data.items():
    religion, created = Religion.objects.get_or_create(name=rel_name)
    if created:
        added_religions += 1
    
    for caste_name in castes:
        caste, c_created = Caste.objects.get_or_create(religion=religion, name=caste_name)
        if c_created:
            added_castes += 1

print(f'Added {added_religions} new religions and {added_castes} new castes.')
