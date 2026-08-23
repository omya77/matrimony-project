from profiles_app.views import enforce_payment
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import InterestRequest, ChatMessage, Notification, BlockList, Report, SavedProfile
from profiles_app.models import Profile
from django.db.models import Q
from django.contrib.auth.models import User
import json

@login_required(login_url='/accounts/login/')
@enforce_payment
def chat(request):
    connections = list(InterestRequest.objects.filter(
        Q(sender=request.user, status='accepted') | Q(receiver=request.user, status='accepted')
    ).select_related('sender__profile', 'receiver__profile'))
    
    # Sort connections by most recent message, fallback to request creation time
    for conn in connections:
        other_user = conn.receiver if conn.sender == request.user else conn.sender
        latest_msg = ChatMessage.objects.filter(
            Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
        ).order_by('-timestamp').first()
        
        # We attach latest_interaction as an attribute to sort by
        conn.latest_interaction = latest_msg.timestamp if latest_msg else conn.created_at

    connections.sort(key=lambda x: x.latest_interaction, reverse=True)
    return render(request, 'web/chat.html', {'connections': connections})

@login_required(login_url='/accounts/login/')
@enforce_payment
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
                    'message': m.message, 'timestamp': m.timestamp.isoformat(), 'is_read': m.is_read
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
                if msg.sender == request.user:
                    msg_id_val = msg.id
                    room_name = '_'.join(map(str, sorted([request.user.id, msg.receiver.id])))
                    msg.delete()
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        f'chat_{room_name}',
                        {
                            'type': 'chat_message',
                            'delete_msg_id': msg_id_val
                        }
                    )
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
            
            from django.db.models import Q
            interest = InterestRequest.objects.filter(
                Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user)
            ).first()
            
            if interest:
                if interest.status == 'pending':
                    if interest.sender == request.user:
                        interest.delete()
                        return JsonResponse({'status': 'cancelled', 'message': 'Interest cancelled successfully!'})
                    else:
                        interest.status = 'accepted'
                        interest.save()
                        # Clean up old notification and send accepted notification
                        Notification.objects.filter(user=request.user, message__contains="sent you an interest request").delete()
                        Notification.objects.create(user=interest.sender, message=f"{request.user.username} accepted your interest request.", link='/interactions/chat/')
                        return JsonResponse({'status': 'accepted', 'message': 'Request accepted!'})
                elif interest.status == 'accepted':
                    return JsonResponse({'status': 'accepted', 'message': 'Already connected!'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Request was previously rejected.'})
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
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            other_user = User.objects.get(id=user_id)
            from django.db.models import Q
            interest = InterestRequest.objects.filter(
                Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
            ).first()
            if interest:
                return JsonResponse({'status': 'success', 'interest_status': interest.status})
            return JsonResponse({'status': 'success', 'interest_status': 'none'})
        except Exception as e: return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)

@csrf_exempt
@login_required(login_url='/accounts/login/')
def api_accept_interest(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            interest = InterestRequest.objects.get(sender_id=data.get('sender_id'), receiver=request.user, status='pending')
            interest.status = 'accepted'
            interest.save()
            # Clean up old notification and send accepted notification
            Notification.objects.filter(user=request.user, message__contains="sent you an interest request").delete()
            Notification.objects.create(user=interest.sender, message=f"{request.user.username} accepted your interest request.", link='/interactions/chat/')
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
def api_save_profile_by_user(request):
    """Legacy alias — looks up profile by user ID (kept for backward compat)."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            profile_user_id = data.get('profile_id')
            profile_to_save = Profile.objects.get(user__id=profile_user_id)

            saved, created = SavedProfile.objects.get_or_create(
                user=request.user,
                profile=profile_to_save
            )

            if not created:
                saved.delete()
                return JsonResponse({'status': 'unsaved', 'message': 'Profile removed from saved.'})
            else:
                return JsonResponse({'status': 'saved', 'message': 'Profile saved successfully!'})

        except Profile.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Profile not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid method.'}, status=405)
            
@csrf_exempt
@login_required(login_url='/accounts/login/')
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            receiver_id = data.get('receiver_id')
            
            # Security Check: Must have an accepted interest request
            has_accepted = InterestRequest.objects.filter(
                (Q(sender=request.user, receiver_id=receiver_id) | Q(sender_id=receiver_id, receiver=request.user)),
                status='accepted'
            ).exists()
            
            if not has_accepted:
                return JsonResponse({'status': 'error', 'message': 'You can only message accepted matches.'}, status=403)
                
            ChatMessage.objects.create(sender=request.user, receiver_id=receiver_id, message=data.get('message'))
            return JsonResponse({'status': 'success'})
        except Exception as e: return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def get_opposite_gender_profiles(request):
    try:
        from interactions_app.models import BlockList
        
        blocked_users_ids = []
        user_profile = None
        if request.user.is_authenticated:
            user_profile = getattr(request.user, 'profile', None)
            # Users blocked by request.user
            blocked_by_me = BlockList.objects.filter(blocker=request.user).values_list('blocked_user_id', flat=True)
            # Users who blocked request.user
            blocked_me = BlockList.objects.filter(blocked_user=request.user).values_list('blocker_id', flat=True)
            blocked_users_ids = list(blocked_by_me) + list(blocked_me)
            
        if not user_profile:
            return Profile.objects.none()

        user_gender = user_profile.gender
        user_religion = user_profile.religion
        user_caste = user_profile.caste
        user_mother_tongue = user_profile.mother_tongue

        base_qs = Profile.objects.none()
        
        # Gender matching logic
        if user_gender == 'Male': 
            base_qs = Profile.objects.filter(gender='Female', payment_status='Paid', approval_status='Approved')
        elif user_gender == 'Female': 
            base_qs = Profile.objects.filter(gender='Male', payment_status='Paid', approval_status='Approved')
        else:
            return Profile.objects.none()
            
        # Enforce strict Religion and Caste matching across all views
        if user_religion:
            base_qs = base_qs.filter(religion=user_religion)
        if user_caste:
            base_qs = base_qs.filter(caste=user_caste)
            
        if blocked_users_ids:
            return base_qs.exclude(user_id__in=blocked_users_ids)
        return base_qs
    except Exception as e:
        print(f"Error in get_opposite_gender_profiles: {e}")
        pass
    return Profile.objects.none()

def attach_interest_status(request, profiles):
    if not request.user.is_authenticated: return profiles
    try:
        from interactions_app.utils import calculate_match_score
        try:
            user_profile = request.user.profile
        except:
            user_profile = None

        sent_requests = dict(InterestRequest.objects.filter(sender=request.user).values_list('receiver_id', 'status'))
        received_requests = dict(InterestRequest.objects.filter(receiver=request.user, status='accepted').values_list('sender_id', 'status'))
        for profile in profiles:
            if profile.user.id in sent_requests: profile.interest_status = sent_requests[profile.user.id]
            elif profile.user.id in received_requests: profile.interest_status = 'accepted'
            
            # Attach AI Match Score
            profile.match_score = calculate_match_score(user_profile, profile)
    except: pass
    return profiles


from datetime import date
from django.core.paginator import Paginator


def save_search_history(request, search_type):
    from interactions_app.models import SearchHistory
    if not request.user.is_authenticated:
        return
    params = dict(request.GET.items())
    if 'page' in params:
        del params['page']
    
    # Check if there is any actual search param
    if any(str(v).strip() for v in params.values()):
        SearchHistory.objects.create(
            user=request.user,
            search_type=search_type,
            query_params=json.dumps(params)
        )

def get_dob_range(min_age, max_age):
    today = date.today()
    max_dob = date(today.year - int(min_age), today.month, today.day)
    min_dob = date(today.year - int(max_age) - 1, today.month, today.day)
    return min_dob, max_dob

@login_required(login_url='/accounts/login/')
@enforce_payment
def basic_search(request):
    matches = get_opposite_gender_profiles(request).exclude(user=request.user)
    
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')
    highest_education = request.GET.get('highest_education')
    city = request.GET.get('city')
    
    if age_min and age_max:
        try:
            min_dob, max_dob = get_dob_range(age_min, age_max)
            matches = matches.filter(dob__range=(min_dob, max_dob))
        except ValueError:
            pass
            
    if highest_education:
        if highest_education == 'Any Other':
            known_educations = ['B.E', 'B.Tech', 'MBA', 'PGDM', 'MBBS', 'BDS', 'B.Com', 'M.Com', 'BCA', 'MCA', 'B.Sc', 'M.Sc', 'B.A', 'M.A']
            for edu in known_educations:
                matches = matches.exclude(highest_education__icontains=edu)
        else:
            # Handle "BCA / MCA" by splitting and matching either
            from django.db.models import Q
            if '/' in highest_education:
                parts = [p.strip() for p in highest_education.split('/')]
                query = Q()
                for p in parts:
                    query |= Q(highest_education__icontains=p)
                matches = matches.filter(query)
            else:
                matches = matches.filter(highest_education__icontains=highest_education)
        
    if city:
        city_clean = city.split(',')[0].strip()
        matches = matches.filter(city__icontains=city_clean)
        
    matches = matches.order_by('-created_at')
    matches = attach_interest_status(request, matches)
    save_search_history(request, 'Basic Search')
    
    paginator = Paginator(matches, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'web/basic_search.html', {'matches': page_obj, 'page_obj': page_obj})

@login_required(login_url='/accounts/login/')
@enforce_payment
def advanced_search(request):
    matches = get_opposite_gender_profiles(request).exclude(user=request.user)
    
    filters = {}
    for key in ['height', 'religion', 'caste', 'mother_tongue', 'profession']:
        val = request.GET.get(key)
        if val:
            filters[f'{key}__icontains'] = val
            
    if filters:
        matches = matches.filter(**filters)
        
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')
    if age_min and age_max:
        try:
            min_dob, max_dob = get_dob_range(age_min, age_max)
            matches = matches.filter(dob__range=(min_dob, max_dob))
        except ValueError:
            pass
            
    highest_education = request.GET.get('highest_education')
    if highest_education:
        if highest_education == 'Any Other':
            known_educations = ['B.E', 'B.Tech', 'MBA', 'PGDM', 'MBBS', 'BDS', 'B.Com', 'M.Com', 'BCA', 'MCA', 'B.Sc', 'M.Sc', 'B.A', 'M.A']
            for edu in known_educations:
                matches = matches.exclude(highest_education__icontains=edu)
        else:
            # Handle "BCA / MCA" by splitting and matching either
            from django.db.models import Q
            if '/' in highest_education:
                parts = [p.strip() for p in highest_education.split('/')]
                query = Q()
                for p in parts:
                    query |= Q(highest_education__icontains=p)
                matches = matches.filter(query)
            else:
                matches = matches.filter(highest_education__icontains=highest_education)
                
    city = request.GET.get('city')
    if city:
        city_clean = city.split(',')[0].strip()
        matches = matches.filter(city__icontains=city_clean)
            
    matches = matches.order_by('-created_at')
    matches = attach_interest_status(request, matches)
    save_search_history(request, 'Advanced Search')
    
    paginator = Paginator(matches, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'web/advanced_search.html', {'matches': page_obj, 'page_obj': page_obj})

import random

@login_required(login_url='/accounts/login/')
@enforce_payment
def ai_search(request):
    try:
        user_profile = request.user.profile
    except:
        user_profile = None

    matches = get_opposite_gender_profiles(request).exclude(user=request.user)
    
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')
    highest_education = request.GET.get('highest_education')
    profession = request.GET.get('profession')
    city = request.GET.get('city')
    
    if age_min and age_max:
        try:
            min_dob, max_dob = get_dob_range(age_min, age_max)
            matches = matches.filter(dob__range=(min_dob, max_dob))
        except ValueError:
            pass
            
    if highest_education:
        if highest_education == 'Any Other':
            known_educations = ['B.E', 'B.Tech', 'MBA', 'PGDM', 'MBBS', 'BDS', 'B.Com', 'M.Com', 'BCA', 'MCA', 'B.Sc', 'M.Sc', 'B.A', 'M.A']
            for edu in known_educations:
                matches = matches.exclude(highest_education__icontains=edu)
        else:
            from django.db.models import Q
            if '/' in highest_education:
                parts = [p.strip() for p in highest_education.split('/')]
                query = Q()
                for p in parts:
                    query |= Q(highest_education__icontains=p)
                matches = matches.filter(query)
            else:
                matches = matches.filter(highest_education__icontains=highest_education)
                
    if profession:
        matches = matches.filter(profession__icontains=profession)
        
    if city:
        city_clean = city.split(',')[0].strip()
        matches = matches.filter(city__icontains=city_clean)
        
    allowed_filters = ['marital_status', 'height', 'religion', 'caste', 'mother_tongue', 'profession', 'income']
    filters = {}
    for key in allowed_filters:
        val = request.GET.get(key)
        if val:
            filters[f"{key}__icontains"] = val
    if filters:
        matches = matches.filter(**filters)
    
    ai_recommendation = request.GET.get('ai_recommendation')
    compatibility_score = request.GET.get('compatibility_score')
    match_percentage = request.GET.get('match_percentage')
    match_reason = request.GET.get('match_reason')

    if ai_recommendation == 'verified':
        matches = matches.filter(approval_status='Approved')
    elif ai_recommendation == 'highly_active':
        matches = matches.order_by('-created_at')
    
    matches = list(matches) 
    
    for m in matches:
        base_score = random.randint(70, 85)
        m.match_reason_text = "AI considers this a solid match for you."
        
        if user_profile:
            if match_reason == 'career':
                if m.profession and m.profession == user_profile.profession: 
                    base_score += 15
                    m.match_reason_text = f"You both work in {m.profession}. High career compatibility!"
                elif m.highest_education and m.highest_education == user_profile.highest_education: 
                    base_score += 10
                    m.match_reason_text = f"You both studied {m.highest_education}. Great educational match."
            elif match_reason == 'lifestyle' or compatibility_score == 'value_match':
                if m.religion and m.religion == user_profile.religion: 
                    base_score += 15
                    m.match_reason_text = "Strong cultural alignment based on religion."
                if m.caste and m.caste == user_profile.caste: 
                    base_score += 10
                    m.match_reason_text = "Shared community background."
            elif match_reason == 'location':
                if m.city and m.city == user_profile.city: 
                    base_score += 20
                    m.match_reason_text = f"You both live in {m.city}! Perfect for meeting up."
                elif m.state and m.state == user_profile.state:
                    base_score += 10
                    m.match_reason_text = f"You both are from {m.state}."
            else:
                # all-rounder logic
                if m.profession == user_profile.profession: 
                    base_score += 5
                    m.match_reason_text = "Career match found."
                if m.city == user_profile.city: 
                    base_score += 5
                    m.match_reason_text = "Location match found."
                if m.religion == user_profile.religion: 
                    base_score += 5
                    m.match_reason_text = "Cultural match found."
        else:
            reasons = ["AI highlights strong communication potential.", "High compatibility based on demographic trends.", "Profile analysis suggests shared lifestyle values."]
            m.match_reason_text = random.choice(reasons)
            
        m.ai_score = min(99, base_score)

    if match_percentage:
        try:
            min_score = int(match_percentage)
            matches = [m for m in matches if m.ai_score >= min_score]
        except ValueError:
            pass
            
    matches = sorted(matches, key=lambda x: (x.ai_score, random.random()), reverse=True)
    matches = attach_interest_status(request, matches)
    save_search_history(request, 'AI Search')
    
    paginator = Paginator(matches, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'web/ai_search.html', {'matches': page_obj, 'page_obj': page_obj})

@login_required(login_url='/accounts/login/')
@enforce_payment
def saved_searches(request):
    from interactions_app.models import SearchHistory
    import json
    histories = list(SearchHistory.objects.filter(user=request.user).order_by('-created_at'))
    
    for h in histories:
        try:
            h.params_dict = json.loads(h.query_params)
            from urllib.parse import urlencode
            h.query_string = urlencode(h.params_dict)
            
            # Create a clean list for the template to avoid custom template filters
            h.clean_params = []
            for k, v in h.params_dict.items():
                if v:
                    clean_key = k.replace('_min', ' Min').replace('_max', ' Max').replace('_', ' ').title()
                    h.clean_params.append({'key': clean_key, 'value': v})
        except:
            h.params_dict = {}
            h.query_string = ""
            h.clean_params = []
            
        if "AI" in h.search_type:
            h.url_slug = "ai"
        elif "Advanced" in h.search_type:
            h.url_slug = "advanced"
        else:
            h.url_slug = "basic"
    
    paginator = Paginator(histories, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'web/saved_searches.html', {'histories': page_obj, 'page_obj': page_obj})

@login_required(login_url='/accounts/login/')
@enforce_payment
def matches1(request):
    matches = get_opposite_gender_profiles(request).exclude(user=request.user)
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
        if profile.religion:
            matches = matches.filter(religion=profile.religion)
        if profile.caste:
            matches = matches.filter(caste=profile.caste)
    
    matches = matches.order_by('-created_at')
    matches = attach_interest_status(request, matches)
    paginator = Paginator(matches, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'web/matches1.html', {'matches': page_obj, 'page_obj': page_obj})

@login_required(login_url='/accounts/login/')
@enforce_payment
def matches2(request):
    matches = get_opposite_gender_profiles(request).exclude(user=request.user)
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
        if profile.religion:
            matches = matches.filter(religion=profile.religion)
        if profile.caste:
            matches = matches.filter(caste=profile.caste)
            
    matches = matches.order_by('created_at')
    matches = attach_interest_status(request, matches)
    paginator = Paginator(matches, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'web/matches2.html', {'matches': page_obj, 'page_obj': page_obj})

@login_required(login_url='/accounts/login/')
@enforce_payment
def nearby_match(request):
    matches = get_opposite_gender_profiles(request).exclude(user=request.user)
    
    age = request.GET.get('age')
    location = request.GET.get('location')
    religion = request.GET.get('religion')
    caste = request.GET.get('caste')
    
    distance = request.GET.get('distance')
    
    if age:
        try:
            if '-' in age:
                min_a, max_a = age.split('-')
                min_dob, max_dob = get_dob_range(min_a.strip(), max_a.strip())
                matches = matches.filter(dob__range=(min_dob, max_dob))
            elif '+' in age:
                min_a = age.replace('+', '').strip()
                min_dob, max_dob = get_dob_range(min_a, "100")
                matches = matches.filter(dob__range=(min_dob, max_dob))
        except:
            pass

    if religion:
        matches = matches.filter(religion__icontains=religion)
    if caste:
        matches = matches.filter(caste__icontains=caste)
    
    # Process Location & Distance
    user_city = request.user.profile.city if hasattr(request.user, 'profile') else None
    user_state = request.user.profile.state if hasattr(request.user, 'profile') else None
    
    target_location = location if location else user_city
    
    if target_location:
        # Extract the primary city name if user typed something like "a.nagar Maharashtra"
        clean_loc = target_location.split(',')[0].strip().split()[0]
        
        if distance:
            dist_val = distance.lower()
            if 'anywhere' in dist_val:
                # No location filter at all
                pass
            elif '100' in dist_val:
                # 100km: simulate by returning all profiles in the target city's state
                target_state = user_state if (not location or (user_city and location.lower() == user_city.lower())) else None
                if not target_state:
                    # Try to lookup the state of the searched city
                    p = Profile.objects.exclude(state__isnull=True).exclude(state='').filter(city__icontains=clean_loc).first()
                    if p: target_state = p.state
                
                if target_state:
                    matches = matches.filter(state__icontains=target_state)
                else:
                    # Fallback to strict city match if state cannot be determined
                    matches = matches.filter(city__icontains=clean_loc)
                    
            elif '50' in dist_val:
                # 50km: simulate by district or city
                target_dist = None
                if hasattr(request.user, 'profile'):
                    target_dist = request.user.profile.district if (not location or (user_city and location.lower() == user_city.lower())) else None
                
                if not target_dist:
                    p = Profile.objects.exclude(district__isnull=True).exclude(district='').filter(city__icontains=clean_loc).first()
                    if p: target_dist = p.district
                
                if target_dist:
                    from django.db.models import Q
                    matches = matches.filter(Q(city__icontains=clean_loc) | Q(district__icontains=target_dist))
                else:
                    matches = matches.filter(city__icontains=clean_loc)
            else:
                # 5km, 10km, 25km: strict city match
                matches = matches.filter(city__icontains=clean_loc)
        else:
            # Default to city match if no distance is specified
            matches = matches.filter(city__icontains=clean_loc)

        
    matches = matches.order_by('-created_at')
    matches = attach_interest_status(request, matches)
    save_search_history(request, 'Nearby Match')
    
    paginator = Paginator(matches, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'web/nearby-match.html', {
        'matches': page_obj, 
        'page_obj': page_obj,
        'target_location': target_location
    })

@login_required(login_url='/accounts/login/')
@enforce_payment
def recomended_matches(request):
    matches = get_opposite_gender_profiles(request).exclude(user=request.user)
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
        filters = Q()
        if profile.pref_religion:
            filters &= Q(religion=profile.pref_religion)
        if profile.pref_age_min and profile.pref_age_max:
            try:
                min_dob, max_dob = get_dob_range(profile.pref_age_min, profile.pref_age_max)
                filters &= Q(dob__range=(min_dob, max_dob))
            except Exception:
                pass
        if filters:
            matches = matches.filter(filters)
            
    matches = matches.order_by('-created_at')
    matches = attach_interest_status(request, matches)
    paginator = Paginator(matches, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'web/recomended-matches.html', {'matches': page_obj, 'page_obj': page_obj})

@login_required(login_url='/accounts/login/')
@enforce_payment
def todays_matches(request):
    from django.utils import timezone
    from datetime import timedelta
    matches = get_opposite_gender_profiles(request).exclude(user=request.user)
    
    # Strictly filter for members who joined within the last 24 hours
    twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
    matches = matches.filter(user__date_joined__gte=twenty_four_hours_ago)
    
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
        if profile.religion:
            matches = matches.filter(religion=profile.religion)
        if profile.caste:
            matches = matches.filter(caste=profile.caste)
            
    matches = matches.order_by('-user__date_joined')
    matches = attach_interest_status(request, matches)
    
    paginator = Paginator(matches, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'web/todays-matches.html', {'matches': page_obj, 'page_obj': page_obj})

def calculate_complex_compatibility(user_profile, match_profile):
    score = 40 # Base score for being an opposite-gender active profile
    reasons = []
    
    # 1. Religion & Caste (High weight: up to 30)
    if user_profile.religion and match_profile.religion:
        if user_profile.religion == match_profile.religion:
            score += 20
            if user_profile.caste and match_profile.caste:
                if user_profile.caste == match_profile.caste:
                    score += 10
                    reasons.append("Community")
                else:
                    score += 2 # Different caste, but same religion
            else:
                reasons.append("Religion")
                
    # 2. Location (State, City: up to 15)
    if user_profile.state and match_profile.state:
        if user_profile.state == match_profile.state:
            score += 5
            if user_profile.city and match_profile.city and user_profile.city == match_profile.city:
                score += 10
                reasons.append("City")
            else:
                reasons.append("State")
                
    # 3. Education & Profession (up to 15)
    if user_profile.highest_education and match_profile.highest_education:
        if user_profile.highest_education == match_profile.highest_education:
            score += 7
            reasons.append("Education")
    if user_profile.profession and match_profile.profession:
        if user_profile.profession == match_profile.profession:
            score += 8
            reasons.append("Profession")

    # 4. Marital Status & Mother Tongue (up to 15)
    if user_profile.marital_status and match_profile.marital_status:
        if user_profile.marital_status == match_profile.marital_status:
            score += 10
    if user_profile.mother_tongue and match_profile.mother_tongue:
        if user_profile.mother_tongue == match_profile.mother_tongue:
            score += 5
            reasons.append("Language")
            
    # 5. Age Preference (up to 5)
    try:
        if user_profile.pref_age_min and user_profile.pref_age_max and match_profile.age:
            if user_profile.pref_age_min <= match_profile.age <= user_profile.pref_age_max:
                score += 5
                reasons.append("Age Preference")
    except:
        pass
        
    score = min(100, score)
    
    if reasons:
        # Construct a nice sentence
        top_reasons = reasons[:3]
        if len(top_reasons) > 1:
            reason_text = f"Highly compatible based on shared {', '.join(top_reasons[:-1])} and {top_reasons[-1]}."
        else:
            reason_text = f"Highly compatible based on shared {top_reasons[0]}."
    else:
        reason_text = "AI considers this a solid match for you based on overall profile analysis."
        
    return score, reason_text

@login_required(login_url='/accounts/login/')
@enforce_payment
def Ai_match(request):
    try:
        user_profile = request.user.profile
    except:
        user_profile = None

    matches = get_opposite_gender_profiles(request).exclude(user=request.user)
    matches_list = list(matches)
    
    if user_profile:
        for match in matches_list:
            score, reason = calculate_complex_compatibility(user_profile, match)
            match.ai_score = score
            match.ai_reason = reason
                
        matches_list = sorted(matches_list, key=lambda x: x.ai_score, reverse=True)
    else:
        for match in matches_list:
            match.ai_score = random.randint(60, 90)
            match.ai_reason = "AI Prediction"
        matches_list = sorted(matches_list, key=lambda x: x.ai_score, reverse=True)

    matches_list = attach_interest_status(request, matches_list)
    
    paginator = Paginator(matches_list, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'web/Ai-match.html', {'matches': page_obj, 'page_obj': page_obj})

@login_required(login_url='/accounts/login/')
@enforce_payment
def featured_brides(request):
    matches = get_opposite_gender_profiles(request).filter(gender='Female').exclude(user=request.user).order_by('-created_at')
    matches = list(matches)
    matches = attach_interest_status(request, matches)

    paginator = Paginator(matches, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'web/featured_brides.html', {'matches': page_obj})

@login_required(login_url='/accounts/login/')
@enforce_payment
def featured_grooms(request):
    matches = get_opposite_gender_profiles(request).filter(gender='Male').exclude(user=request.user).order_by('-created_at')
    matches = list(matches)
    matches = attach_interest_status(request, matches)

    paginator = Paginator(matches, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'web/featured_grooms.html', {'matches': page_obj})

@csrf_exempt
@login_required(login_url='/accounts/login/')
def api_report_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reported_user_id = data.get('reported_user_id')
            reason = data.get('reason')
            
            if reported_user_id and reason:
                from interactions_app.models import Report
                from django.contrib.auth.models import User
                reported_user = User.objects.get(id=reported_user_id)
                Report.objects.create(
                    reporter=request.user,
                    reported_user=reported_user,
                    reason=reason
                )
                return JsonResponse({'status': 'success', 'message': 'Report submitted successfully. We will review this profile.'})
            return JsonResponse({'status': 'error', 'message': 'Missing data.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@login_required(login_url='/accounts/login/')
def api_navbar_counts(request):
    try:
        from interactions_app.models import InterestRequest, ChatMessage, Notification
        unread_requests = InterestRequest.objects.filter(receiver=request.user, status='pending', is_viewed=False).count()
        unread_messages = ChatMessage.objects.filter(receiver=request.user, is_read=False, deleted_by_receiver=False).count()
        return JsonResponse({
            'status': 'success',
            'unread_requests_count': unread_requests,
            'unread_messages_count': unread_messages
        })
    except Exception as e:
        return JsonResponse({'status': 'error'}, status=400)

from .models import ProfileVisit

@login_required(login_url='/accounts/login/')
@csrf_exempt
def api_log_visit(request, user_id):
    if request.method == 'POST':
        try:
            viewed_user = User.objects.get(id=user_id)
            viewed_profile = viewed_user.profile
            # Only log if viewing someone else
            if request.user != viewed_user:
                ProfileVisit.objects.create(viewer=request.user, viewed_profile=viewed_profile)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid method'})

