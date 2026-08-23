import re

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\admin_panel\urls.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

if 'path(\'login/\',' not in content:
    content = content.replace('urlpatterns = [', 'urlpatterns = [\n    path(\'login/\', views.admin_login, name=\'admin_login\'),\n    path(\'logout/\', views.admin_logout, name=\'admin_logout\'),\n')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Update logout link in base_admin.html
base_admin = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\admin_panel\base_admin.html'
with open(base_admin, 'r', encoding='utf-8') as f:
    html = f.read()
    
html = html.replace('href="/" class="nav-item text-danger"', 'href="{% url \'admin_logout\' %}" class="nav-item text-danger"')
with open(base_admin, 'w', encoding='utf-8') as f:
    f.write(html)
