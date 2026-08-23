import os
import sys
import django

sys.path.append(r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony-2807-2\Matrimony\Matrimony')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Matrimony.settings')
django.setup()

from django.core.mail import send_mail

try:
    send_mail(
        'Test OTP',
        'Your OTP for registration is: 1234',
        'foreverbond137@gmail.com',
        ['foreverbond137@gmail.com'],
        fail_silently=False,
    )
    print("SUCCESS: Email sent!")
except Exception as e:
    print("FAILED:", str(e))
