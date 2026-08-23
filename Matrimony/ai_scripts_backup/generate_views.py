import os

views_content = '''from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import InterestRequest, ChatMessage, Notification, BlockList, Report, SavedProfile
from profiles_app.models import Profile
from django.db.models import Q
from django.contrib.auth.models import User
import json

@login_required(login_url='/accounts/login/')
def chat(request):
    connections = InterestRequest.objects.filter(
        Q(sender=request.user, status='accepted') | Q(receiver=request.user, status='accepted')
    ).select_related('sender__profile', 'receiver__profile')
    return render(request, 'web/chat.html', {'connections': connections})

@login_required(login_url='/accounts/login/')
def requests(request):
    pending_received = InterestRequest.objects.filter(receiver=request.user, status='pending').order_by('-created_at')
    return render(request, 'web/requests.html', {'pending_received': pending_received})

@login_required(login_url='/accounts/login/')
def gestures(request):
    return render(request, 'web/gestures.html')

@login_required(login_url='/accounts/login/')
def fetch_messages(request, user_id):
    if request.method == 'GET':
        try:
            interest = InterestRequest.objects.filter(
                (Q(sender=request.user, receiver_id=user_id) | Q(sender_id=user_id, receiver=request.user)),
                status='accepted'
            ).exists()
            if not interest:
                return JsonResponse({'status': 'error', 'message': 'You cannot view chats for this user.'}, status=403)
            messages = ChatMessage.objects.filter(
                (Q(sender=request.user, receiver_id=user_id) | Q(sender_id=user_id, receiver=request.user))
            ).order_by('timestamp')
            unread_msgs = messages.filter(receiver=request.user, is_read=False)
            unread_msgs.update(is_read=True)
            msgs_data = []
            for m in messages:
                if m.sender == request.user and getattr(m, 'deleted_by_sender', False): continue
                if m.receiver == request.user and getattr(m, 'deleted_by_receiver', False): continue
                msgs_data.append({
                    'id': m.id, 'sender_id': m.sender.id, 'is_outgoing': m.sender == request.user,
                    'message': m.message, 'timestamp': m.timestamp.isoformat()
                })
            return JsonResponse({'status': 'success', 'messages': msgs_data})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@csrf_exempt
@login_required(login_url='/accounts/login/')
def api_save_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            profile_id = data.get('profile_id')
            if not profile_id: return JsonResponse({'status': 'error', 'message': 'Profile ID required.'}, status=400)
            from interactions_app.models import SavedProfile
            from profiles_app.models import Profile
            profile_to_save = Profile.objects.get(id=profile_id)
            saved_profile, created = SavedProfile.objects.get_or_create(user=request.user, profile=profile_to_save)
            if not created:
                saved_profile.delete()
                return JsonResponse({'status': 'unsaved', 'message': 'Profile removed from saved.'})
            return JsonResponse({'status': 'saved', 'message': 'Profile saved successfully!'})
        except Profile.DoesNotExist: return JsonResponse({'status': 'error', 'message': 'Profile not found.'}, status=404)
        except Exception as e: return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@csrf_exempt
@login_required(login_url='/accounts/login/')
def api_delete_chat(request, user_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.body else {}
            delete_type = data.get('delete_type', 'for_me')
            other_user = User.objects.get(id=user_id)
            messages = ChatMessage.objects.filter(
                Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
            )
            if delete_type == 'for_me':
                for msg in messages:
                    if msg.sender == request.user: msg.deleted_by_sender = True
                    if msg.receiver == request.user: msg.deleted_by_receiver = True
                    msg.save()
                return JsonResponse({'status': 'success', 'message': 'Chat deleted for you.'})
        except User.DoesNotExist: return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)
        except Exception as e: return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@csrf_exempt
@login_required(login_url='/accounts/login/')
def api_mark_notifications_read(request):
    if request.method == 'POST':
        try:
            Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
            return JsonResponse({'status': 'success'})
        except Exception as e: return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error'}, status=405)

@login_required
def block_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            blocked = User.objects.get(id=data.get('user_id'))
            BlockList.objects.get_or_create(blocker=request.user, blocked_user=blocked)
            return JsonResponse({'status': 'success', 'message': 'User blocked successfully.'})
        except: return JsonResponse({'status': 'error', 'message': 'Error'})
    return JsonResponse({'status': 'error'})

@login_required
def report_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            reported = User.objects.get(id=data.get('user_id'))
            Report.objects.create(reporter=request.user, reported_user=reported, reason=data.get('reason', 'Reason'))
            return JsonResponse({'status': 'success', 'message': 'User reported successfully.'})
        except: return JsonResponse({'status': 'error', 'message': 'Error'})
    return JsonResponse({'status': 'error'})

@csrf_exempt
@login_required(login_url='/accounts/login/')
def api_delete_message(request, msg_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.body else {}
            delete_type = data.get('delete_type', 'for_me')
            msg = ChatMessage.objects.get(id=msg_id)
            if delete_type == 'for_me':
                if msg.sender == request.user: msg.deleted_by_sender = True
                elif msg.receiver == request.user: msg.deleted_by_receiver = True
                msg.save()
            elif delete_type == 'for_everyone':
                if msg.sender == request.user: msg.delete()
            return JsonResponse({'status': 'success', 'message': 'Message deleted successfully.'})
        except ChatMessage.DoesNotExist: return JsonResponse({'status': 'error', 'message': 'Message not found.'}, status=404)
        except Exception as e: return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method.'}, status=405)

@csrf_exempt
@login_required(login_url='/accounts/login/')
def api_express_interest(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            receiver = User.objects.get(id=data.get('receiver_id'))
            if receiver == request.user: return JsonResponse({'status': 'error', 'message': 'Cannot send interest to yourself.'}, status=400)
            interest = InterestRequest.objects.filter(sender=request.user, receiver=receiver).first()
            if interest:
                interest.delete()
                return JsonResponse({'status': 'cancelled', 'message': 'Interest cancelled successfully!'})
            else:
                interest = InterestRequest.objects.create(sender=request.user, receiver=receiver, status='pending')
                Notification.objects.create(user=receiver, message=f"{request.user.username} sent you an interest request.", link='/interactions/requests/')
                return JsonResponse({'status': 'pending', 'message': 'Interest sent successfully!'})
        except User.DoesNotExist: return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)
        except Exception as e: return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error'}, status=405)

@csrf_exempt
@login_required(login_url='/accounts/login/')
def api_check_interest(request):
    return JsonResponse({'status': 'success'})

@csrf_exempt
@login_required(login_url='/accounts/login/')
def api_accept_interest(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            interest = InterestRequest.objects.get(sender_id=data.get('sender_id'), receiver=request.user, status='pending')
            interest.status = 'accepted'
            interest.save()
            return JsonResponse({'status': 'accepted', 'message': 'Request accepted.'})
        except Exception as e: return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)

@csrf_exempt
@login_required(login_url='/accounts/login/')
def api_reject_interest(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            interest = InterestRequest.objects.get(sender_id=data.get('sender_id'), receiver=request.user, status='pending')
            interest.status = 'rejected'
            interest.save()
            return JsonResponse({'status': 'rejected', 'message': 'Request rejected.'})
        except Exception as e: return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)
            
@csrf_exempt
@login_required(login_url='/accounts/login/')
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ChatMessage.objects.create(sender=request.user, receiver_id=data.get('receiver_id'), message=data.get('message'))
            return JsonResponse({'status': 'success'})
        except: return JsonResponse({'status': 'error'}, status=400)

def get_opposite_gender_profiles(request):
    try:
        user_gender = request.user.profile.gender
        if user_gender == 'Male': return Profile.objects.filter(gender='Female')
        elif user_gender == 'Female': return Profile.objects.filter(gender='Male')
    except: pass
    return Profile.objects.all()

def attach_interest_status(request, profiles):
    if not request.user.is_authenticated: return profiles
    try:
        sent_requests = dict(InterestRequest.objects.filter(sender=request.user).values_list('receiver_id', 'status'))
        received_requests = dict(InterestRequest.objects.filter(receiver=request.user, status='accepted').values_list('sender_id', 'status'))
        for profile in profiles:
            if profile.user.id in sent_requests: profile.interest_status = sent_requests[profile.user.id]
            elif profile.user.id in received_requests: profile.interest_status = 'accepted'
    except: pass
    return profiles

'''

with open('interactions_app/views.py', 'w', encoding='utf-8') as f:
    f.write(views_content)

# Add search views from temp_profiles.py
with open('temp_profiles.py', 'r', encoding='utf-8') as f:
    profiles_views = f.read()

start_idx = profiles_views.find('def basic_search(request):')
end_idx = profiles_views.find('def personal(request):')
if start_idx != -1 and end_idx != -1:
    extracted = profiles_views[start_idx:end_idx]
    with open('interactions_app/views.py', 'a', encoding='utf-8') as f:
        f.write('\n' + extracted)
    print('Fully reconstructed views.py with search views included!')
else:
    print('ERROR extracting search views!')
