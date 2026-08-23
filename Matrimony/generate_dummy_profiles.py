import os
import django
import random
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Matrimony.settings')
django.setup()

from django.contrib.auth.models import User
from profiles_app.models import Profile

castes_list = [
    ("Hindu", ["Brahmin", "Maratha", "Rajput", "Baniya", "Yadav", "Kunbi", "Kayastha", "Lingayat"]),
    ("Muslim", ["Sunni", "Shia", "Pathan", "Syed", "Sheikh"]),
    ("Christian", ["Catholic", "Protestant", "Orthodox"]),
    ("Sikh", ["Jat", "Khatri", "Arora", "Ramgarhia"])
]

first_names_m = ["Aarav", "Vihaan", "Aditya", "Rohan", "Kabir", "Aryan", "Dhruv", "Ishaan", "Karan", "Rahul"]
first_names_f = ["Aanya", "Diya", "Sanya", "Priya", "Kavya", "Riya", "Ananya", "Myra", "Sneha", "Neha"]
last_names = ["Sharma", "Patil", "Deshmukh", "Singh", "Gupta", "Khan", "Syed", "Thomas", "Kaur", "Gill"]

cities = ["Mumbai", "Pune", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Ahmedabad"]
professions = ["Software Engineer", "Doctor", "Teacher", "Business", "Architect", "Banker", "CA"]

print(f'Starting profile generation...')

def random_date(start_year=1985, end_year=2001):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return date(year, month, day)

for rel, castes in castes_list:
    for caste in castes:
        for gender in ['Male', 'Female']:
            for i in range(2): # 2 of each gender per caste = 4 per caste
                is_male = gender == 'Male'
                fname = random.choice(first_names_m) if is_male else random.choice(first_names_f)
                lname = random.choice(last_names)
                username = f"{fname.lower()}_{caste.lower()}_{random.randint(100,999)}"
                email = f"{username}@example.com"
                
                try:
                    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
                    if created:
                        user.set_password('password123')
                        user.save()
                        
                        Profile.objects.create(
                            user=user,
                            full_name=f"{fname} {lname}",
                            gender=gender,
                            dob=random_date(),
                            religion=rel,
                            caste=caste,
                            city=random.choice(cities),
                            profession=random.choice(professions),
                            is_photo_approved=True,
                            approval_status='Approved'
                        )
                except Exception as e:
                    pass

print(f'Total Users: {User.objects.count()}')
print(f'Total Profiles: {Profile.objects.count()}')
