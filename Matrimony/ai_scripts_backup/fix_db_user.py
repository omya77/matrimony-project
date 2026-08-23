import os

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Matrimony\settings.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("'USER': 'uogglwhiaeob9ele'", "'USER': 'uogg1whiaeob9ele'")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Username fixed in settings.py')
