import re

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\interactions_app\views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update fetch_messages to mark messages as read
old_fetch = '''            messages = ChatMessage.objects.filter(
                (Q(sender=request.user, receiver_id=user_id) | Q(sender_id=user_id, receiver=request.user))
            ).order_by('timestamp')
            
            msgs_data = []
            for m in messages:
                # Skip messages deleted by current user'''

new_fetch = '''            messages = ChatMessage.objects.filter(
                (Q(sender=request.user, receiver_id=user_id) | Q(sender_id=user_id, receiver=request.user))
            ).order_by('timestamp')
            
            # Mark unread messages sent to the current user as read
            unread_msgs = messages.filter(receiver=request.user, is_read=False)
            unread_msgs.update(is_read=True)
            
            msgs_data = []
            for m in messages:
                # Skip messages deleted by current user'''
content = content.replace(old_fetch, new_fetch)

# 2. Update api_express_interest to send a notification
old_express = '''                    interest.status = 'pending'
                    interest.save()
                    
            return JsonResponse({'status': 'pending', 'message': 'Interest sent successfully!'})'''

new_express = '''                    interest.status = 'pending'
                    interest.save()
                    
            from .models import Notification
            Notification.objects.create(
                user=receiver,
                message=f"{request.user.profile.full_name or request.user.username} sent you an interest request.",
                link='/interactions/requests/'
            )
                    
            return JsonResponse({'status': 'pending', 'message': 'Interest sent successfully!'})'''
content = content.replace(old_express, new_express)

# 3. Update api_accept_interest to send a notification
old_accept = '''            if interest:
                interest.status = 'accepted'
                interest.save()
                return JsonResponse({'status': 'accepted', 'message': 'Interest accepted!'})'''

new_accept = '''            if interest:
                interest.status = 'accepted'
                interest.save()
                
                from .models import Notification
                Notification.objects.create(
                    user=interest.sender,
                    message=f"{request.user.profile.full_name or request.user.username} accepted your interest request!",
                    link='/interactions/chat/'
                )
                
                return JsonResponse({'status': 'accepted', 'message': 'Interest accepted!'})'''
content = content.replace(old_accept, new_accept)

# 4. Add api_mark_notifications_read
new_api = '''
@csrf_exempt
@login_required(login_url='/accounts/login/')
def api_mark_notifications_read(request):
    if request.method == 'POST':
        try:
            from .models import Notification
            Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error'}, status=405)
'''
if 'def api_mark_notifications_read' not in content:
    content += new_api

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated views.py")
