import sys
with open('c:\\Users\\Omkar\\Desktop\\Matrimony_regis omkar\\Matrimony_regis omkar\\Matrimony-2807-2\\Matrimony\\Matrimony\\accounts_app\\views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
with open('c:\\Users\\Omkar\\Desktop\\Matrimony_regis omkar\\Matrimony_regis omkar\\Matrimony-2807-2\\Matrimony\\Matrimony\\accounts_app\\views.py', 'w', encoding='utf-8') as f:
    for line in lines:
        if '[EMAIL OTP]' not in line and 'FREE DEV MODE' not in line:
            f.write(line)
