import os

files = [
    r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web\featured_brides.html',
    r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web\featured_grooms.html',
    r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web\verified_profiles.html'
]

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if '{% load interaction_tags %}' not in content:
        # These files start with <!doctype html> or {% extends ... %}
        # If they don't have block content, just put it at the very top
        content = '{% load interaction_tags %}\n' + content

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print('Added load tags to templates.')
