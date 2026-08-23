import os

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\interactions_app\urls.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_path = "    path('api/mark-notifications-read/', views.api_mark_notifications_read, name='api_mark_notifications_read'),\n"

if 'api/mark-notifications-read/' not in content:
    content = content.replace("path('api/delete-chat/<int:user_id>/', views.api_delete_chat, name='api_delete_chat'),", 
                              "path('api/delete-chat/<int:user_id>/', views.api_delete_chat, name='api_delete_chat'),\n" + new_path)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated urls.py")
else:
    print("Already updated urls.py")
