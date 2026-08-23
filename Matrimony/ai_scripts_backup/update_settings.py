import os

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Matrimony\settings.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add daphne and channels to INSTALLED_APPS
if "'daphne'" not in content:
    content = content.replace('INSTALLED_APPS = [', "INSTALLED_APPS = [\n    'daphne',")
if "'channels'" not in content:
    content = content.replace('INSTALLED_APPS = [', "INSTALLED_APPS = [\n    'channels',")

# Update ASGI_APPLICATION
if 'ASGI_APPLICATION' not in content:
    content += "\nASGI_APPLICATION = 'Matrimony.asgi.application'\n"

# Update CHANNEL_LAYERS
if 'CHANNEL_LAYERS' not in content:
    content += '''
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}
'''
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated settings.py for Channels')
