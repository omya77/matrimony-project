import os

context_processors_path = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\interactions_app\context_processors.py'

new_cp_code = '''from interactions_app.models import InterestRequest, ChatMessage, Notification

def navbar_badges(request):
    """
    Context processor to inject unread requests count into all templates.
    """
    if request.user.is_authenticated:
        unread_requests_count = InterestRequest.objects.filter(receiver=request.user, status='pending').count()
        unread_messages_count = ChatMessage.objects.filter(receiver=request.user, is_read=False, deleted_by_receiver=False).count()
        unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
        
        return {
            'unread_requests_count': unread_requests_count,
            'unread_messages_count': unread_messages_count,
            'unread_notifications_count': unread_notifications_count,
            'notifications': notifications
        }
    return {
        'unread_requests_count': 0,
        'unread_messages_count': 0,
        'unread_notifications_count': 0,
        'notifications': []
    }
'''

with open(context_processors_path, 'w', encoding='utf-8') as f:
    f.write(new_cp_code)
print("Updated context_processors.py")
