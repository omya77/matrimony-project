import re

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\admin_panel\base_admin.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace static profile block with dynamic one
old_profile_block = '''<div class="user-profile ms-3 border-start ps-3">
                    <img src="https://ui-avatars.com/api/?name=Super+Admin&background=1e293b&color=fff" alt="Admin">
                    <div class="user-info">
                        <span class="name">Hi, Admin!</span>
                        <span class="role">Super Admin</span>
                    </div>
                </div>'''

new_profile_block = '''<div class="user-profile ms-3 border-start ps-3">
                    <img src="{% if request.user.profile.profile_photo %}{{ request.user.profile.profile_photo.url }}{% else %}https://ui-avatars.com/api/?name={{ request.user.first_name|default:request.user.username }}&background=1e293b&color=fff{% endif %}" alt="Admin">
                    <div class="user-info">
                        <span class="name">Hi, {{ request.user.first_name|default:request.user.username }}!</span>
                        <span class="role">
                            {% if request.user.is_superuser %} Super Admin 
                            {% elif request.user.is_staff %} Support Staff 
                            {% else %} Admin {% endif %}
                        </span>
                    </div>
                </div>'''

content = content.replace(old_profile_block, new_profile_block)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Profile block made dynamic.')
