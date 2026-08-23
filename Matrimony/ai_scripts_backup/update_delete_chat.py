import os
import re

views_path = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\interactions_app\views.py'

with open(views_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update fetch_messages
old_fetch = '''            messages = ChatMessage.objects.filter(
                (Q(sender=request.user, receiver_id=user_id) | Q(sender_id=user_id, receiver=request.user))
            ).order_by('timestamp')
            
            msgs_data = []
            for m in messages:
                msgs_data.append({
                    'sender_id': m.sender.id,
                    'is_outgoing': m.sender == request.user,
                    'message': m.message,
                    'timestamp': m.timestamp.isoformat()
                })'''

new_fetch = '''            messages = ChatMessage.objects.filter(
                (Q(sender=request.user, receiver_id=user_id) | Q(sender_id=user_id, receiver=request.user))
            ).order_by('timestamp')
            
            msgs_data = []
            for m in messages:
                # Skip messages deleted by current user
                if m.sender == request.user and m.deleted_by_sender:
                    continue
                if m.receiver == request.user and m.deleted_by_receiver:
                    continue
                    
                msgs_data.append({
                    'sender_id': m.sender.id,
                    'is_outgoing': m.sender == request.user,
                    'message': m.message,
                    'timestamp': m.timestamp.isoformat()
                })'''

content = content.replace(old_fetch, new_fetch)

# 2. Update api_delete_chat
old_delete = '''@csrf_exempt
@login_required(login_url='/accounts/login/')
def api_delete_chat(request, user_id):
    if request.method == 'POST':
        try:
            from .models import ChatMessage
            from django.db.models import Q
            other_user = User.objects.get(id=user_id)
            ChatMessage.objects.filter(
                Q(sender=request.user, receiver=other_user) | 
                Q(sender=other_user, receiver=request.user)
            ).delete()
            return JsonResponse({'status': 'success', 'message': 'Chat deleted successfully.'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)'''

new_delete = '''@csrf_exempt
@login_required(login_url='/accounts/login/')
def api_delete_chat(request, user_id):
    if request.method == 'POST':
        try:
            import json
            data = {}
            if request.body:
                data = json.loads(request.body)
            delete_type = data.get('delete_type', 'for_me')
            
            from .models import ChatMessage
            from django.db.models import Q
            from django.contrib.auth.models import User
            other_user = User.objects.get(id=user_id)
            
            messages = ChatMessage.objects.filter(
                Q(sender=request.user, receiver=other_user) | 
                Q(sender=other_user, receiver=request.user)
            )
            
            if delete_type == 'for_everyone':
                # Hard delete all messages in conversation
                messages.delete()
                return JsonResponse({'status': 'success', 'message': 'Chat deleted for everyone.'})
            else:
                # Soft delete for current user
                for msg in messages:
                    if msg.sender == request.user:
                        msg.deleted_by_sender = True
                    if msg.receiver == request.user:
                        msg.deleted_by_receiver = True
                    msg.save()
                return JsonResponse({'status': 'success', 'message': 'Chat deleted for you.'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)'''

content = content.replace(old_delete, new_delete)

with open(views_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated backend for chat deletion")
