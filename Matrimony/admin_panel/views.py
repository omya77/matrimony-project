from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.http import JsonResponse
from profiles_app.models import Profile
import json
import urllib.parse
from django.views.decorators.csrf import csrf_exempt

import datetime
from django.utils import timezone
import json


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages

def admin_login(request):
    next_url = request.GET.get('next') or request.POST.get('next') or 'admin_dashboard'
    
    if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
        return redirect(next_url) if next_url.startswith('/') else redirect('admin_dashboard')
        
    if request.method == 'POST':
        email_or_username = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        from django.contrib.auth.models import User
        
        username_to_auth = email_or_username
        if '@' in email_or_username:
            u_obj = User.objects.filter(email__iexact=email_or_username).first()
            if u_obj:
                username_to_auth = u_obj.username

        user = authenticate(request, username=username_to_auth, password=password)
        
        if user is not None and (user.is_superuser or user.is_staff):
            login(request, user)
            return redirect(next_url) if next_url.startswith('/') else redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
            
    return render(request, 'admin_panel/admin_login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

import random
from django.core.mail import send_mail
from django.conf import settings

def admin_forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        from django.contrib.auth.models import User
        user = User.objects.filter(email__iexact=email, is_staff=True).first() or User.objects.filter(username__iexact=email, is_staff=True).first()
        if user:
            otp = str(random.randint(100000, 999999))
            request.session['admin_otp'] = otp
            request.session['admin_otp_user_id'] = user.id
            try:
                send_mail(
                    'Admin Password Reset OTP',
                    f'Your OTP for password reset is: {otp}',
                    settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'admin@example.com',
                    [user.email if user.email else email],
                    fail_silently=True,
                )
            except Exception as e:
                pass
            return redirect('admin_verify_otp')
        else:
            messages.error(request, 'No admin account found with that email.')
    return render(request, 'admin_panel/admin_forgot_password.html')

def admin_verify_otp(request):
    if 'admin_otp' not in request.session:
        return redirect('admin_forgot_password')
        
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '').strip()
        if entered_otp == request.session.get('admin_otp'):
            request.session['admin_otp_verified'] = True
            return redirect('admin_reset_password')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'admin_panel/admin_verify_otp.html')

def admin_reset_password(request):
    if not request.session.get('admin_otp_verified'):
        return redirect('admin_login')
        
    if request.method == 'POST':
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        if password and password == confirm_password:
            from django.contrib.auth.models import User
            user_id = request.session.get('admin_otp_user_id')
            try:
                user = User.objects.get(id=user_id)
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successful! Please login.')
                
                # Cleanup
                for key in ['admin_otp', 'admin_otp_user_id', 'admin_otp_verified']:
                    if key in request.session:
                        del request.session[key]
                return redirect('admin_login')
            except Exception:
                messages.error(request, 'Error resetting password.')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'admin_panel/admin_reset_password.html')

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def dashboard(request):
    try:
        from interactions_app.models import InterestRequest
        matches_made = InterestRequest.objects.filter(status='accepted').count()
    except Exception:
        matches_made = 0

    total_users = Profile.objects.filter(user__is_superuser=False, user__is_staff=False).count()
    active_users = Profile.objects.filter(user__is_superuser=False, user__is_staff=False, approval_status='Approved').count()
    male_users = Profile.objects.filter(user__is_superuser=False, user__is_staff=False, gender__iexact='Male').count()
    female_users = Profile.objects.filter(user__is_superuser=False, user__is_staff=False, gender__iexact='Female').count()
    premium_users = Profile.objects.filter(user__is_superuser=False, user__is_staff=False, payment_status='Paid').count()
    
    # Calculate real revenue from successful transactions
    from django.db.models import Sum
    try:
        from payments_app.models import Transaction
        total_revenue = Transaction.objects.filter(status='Success').aggregate(total=Sum('amount'))['total'] or 0
    except Exception:
        total_revenue = 0
        
    recent_profiles = Profile.objects.select_related('user').filter(user__is_superuser=False, user__is_staff=False).exclude(gender__isnull=True).exclude(gender__exact='').order_by('-created_at')[:5]
    recent_approvals = Profile.objects.select_related('user').filter(user__is_superuser=False, user__is_staff=False, approval_status='Approved').exclude(gender__isnull=True).exclude(gender__exact='').order_by('-updated_at')[:3]

    today = timezone.now().date()
    labels = []
    data = []
    for i in range(6, -1, -1):
        day = today - datetime.timedelta(days=i)
        labels.append(day.strftime('%d %b'))
        count = Profile.objects.filter(user__is_superuser=False, user__is_staff=False, created_at__date=day).count()
        data.append(count)
        
    # Build mixed recent activities
    activities = []
    for p in recent_profiles[:3]:
        activities.append({
            'type': 'register',
            'text': f"New user {p.full_name or p.user.username} registered",
            'time': p.created_at
        })
    for p in recent_approvals:
        activities.append({
            'type': 'approve',
            'text': f"Profile of {p.full_name or p.user.username} approved",
            'time': p.updated_at
        })
    # Sort activities by time descending
    activities.sort(key=lambda x: x['time'], reverse=True)
    recent_activities = activities[:5]

    context = {
        'total_users': total_users,
        'active_users': active_users,
        'male_users': male_users,
        'female_users': female_users,
        'premium_users': premium_users,
        'total_revenue': total_revenue,
        'matches_made': matches_made,
        'recent_profiles': recent_profiles,
        'recent_activities': recent_activities,
        'chart_labels': json.dumps(labels),
        'chart_data': json.dumps(data),
    }
    return render(request, 'admin_panel/dashboard.html', context)

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def profile_approvals(request):
    approved_profiles = Profile.objects.select_related('user').filter(user__is_superuser=False, user__is_staff=False, approval_status='Approved').order_by('-updated_at')
    pending_profiles = Profile.objects.select_related('user').filter(user__is_superuser=False, user__is_staff=False, approval_status='Pending').exclude(gender__isnull=True).exclude(gender__exact='').order_by('-created_at')
    context = {
        'approved_profiles': approved_profiles,
        'pending_profiles': pending_profiles
    }
    return render(request, 'admin_panel/profile_approvals.html', context)

@csrf_exempt
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def approve_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            profile_id = data.get('profile_id')
            try:
                profile = Profile.objects.get(id=profile_id)
            except Profile.DoesNotExist:
                return JsonResponse({'status': 'success', 'message': 'Action already completed.'})
            
            # Generate matrimony_id (e.g. FB0001) filling gaps
            existing_ids = Profile.objects.filter(user__is_superuser=False, user__is_staff=False, matrimony_id__startswith='FB').values_list('matrimony_id', flat=True)
            used_nums = set()
            for eid in existing_ids:
                try:
                    used_nums.add(int(eid[2:]))
                except ValueError:
                    pass
            
            new_num = 1
            while new_num in used_nums:
                new_num += 1
                
            new_id = f"FB{new_num:04d}"
            
            profile.approval_status = 'Approved'
            profile.matrimony_id = new_id
            profile.save()
            
            # Generate WhatsApp Link
            mobile = profile.mobile
            if not mobile:
                mobile = profile.user.username
                
            if not mobile.startswith('+'):
                if len(mobile) == 10:
                    mobile = "91" + mobile
                else:
                    mobile = mobile.lstrip('0')
            else:
                mobile = mobile.replace('+', '')
                
            name = profile.full_name or "User"
            payment_link = request.build_absolute_uri(f"/payments/pay_link/{profile.user.id}/")
            msg = f"Hello {name},\n\nCongratulations! Your profile registration on ForeverBond Matrimony has been successfully approved by the admin. 🎉\n\nTo get full access to all profiles and features, please complete your payment using the secure link below:\n{payment_link}\n\nOnce your payment is completed, you can directly go to the login page, enter your username and password, and enjoy full access to all pages and features on ForeverBond!"
            
            whatsapp_url = f"https://api.whatsapp.com/send/?phone={mobile}&text={urllib.parse.quote(msg)}"
            
            return JsonResponse({'status': 'success', 'message': 'User approved.', 'whatsapp_url': whatsapp_url})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@csrf_exempt
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def reject_user(request):
    """Reject and delete user so they can re-register with the same email."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            profile_id = data.get('profile_id')
            try:
                profile = Profile.objects.get(id=profile_id)
            except Profile.DoesNotExist:
                return JsonResponse({'status': 'success', 'message': 'User already rejected or deleted.'})
            try:
                user = profile.user
            except Exception:
                user = None
            
            try:
                if user:
                    from interactions_app.models import InterestRequest
                    InterestRequest.objects.filter(sender=user).delete()
                    InterestRequest.objects.filter(receiver=user).delete()
            except Exception:
                pass
            
            try:
                profile.delete()
            except Exception:
                pass
            
            if user:
                try:
                    user.delete()
                except Exception as e:
                    from django.db import connection
                    with connection.cursor() as cursor:
                        if connection.vendor == 'sqlite':
                            cursor.execute("PRAGMA foreign_keys = OFF;")
                        else:
                            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
                        try:
                            cursor.execute("DELETE FROM interactions_app_interestrequest WHERE sender_id = %s OR receiver_id = %s", [user.id, user.id])
                        except Exception:
                            pass
                        try:
                            cursor.execute("DELETE FROM profiles_app_profile WHERE id = %s", [profile_id])
                        except Exception:
                            pass
                        try:
                            cursor.execute("DELETE FROM auth_user WHERE id = %s", [user.id])
                        except Exception:
                            pass
                        if connection.vendor == 'sqlite':
                            cursor.execute("PRAGMA foreign_keys = ON;")
                        else:
                            cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
            else:
                try:
                    from django.db import connection
                    with connection.cursor() as cursor:
                        if connection.vendor == 'sqlite':
                            cursor.execute("PRAGMA foreign_keys = OFF;")
                        else:
                            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
                        cursor.execute("DELETE FROM profiles_app_profile WHERE id = %s", [profile_id])
                        if connection.vendor == 'sqlite':
                            cursor.execute("PRAGMA foreign_keys = ON;")
                        else:
                            cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
                except Exception:
                    pass
            
            return JsonResponse({'status': 'success', 'message': 'User rejected and removed. They can re-register.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@csrf_exempt
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def delete_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            profile_id = data.get('profile_id')
            try:
                profile = Profile.objects.get(id=profile_id)
            except Profile.DoesNotExist:
                return JsonResponse({'status': 'success', 'message': 'User already deleted.'})
            try:
                user = profile.user
            except Exception:
                user = None
            
            try:
                if user:
                    # First, delete all related InterestRequest records
                    from interactions_app.models import InterestRequest
                    InterestRequest.objects.filter(sender=user).delete()
                    InterestRequest.objects.filter(receiver=user).delete()
            except Exception:
                pass
            
            try:
                # Delete the profile explicitly
                profile.delete()
            except Exception:
                pass
            
            if user:
                try:
                    # Delete the user (this also cascades to any remaining related objects)
                    user.delete()
                except Exception as e:
                    # Fallback to raw SQL with FK checks disabled to force delete
                    from django.db import connection
                    with connection.cursor() as cursor:
                        if connection.vendor == 'sqlite':
                            cursor.execute("PRAGMA foreign_keys = OFF;")
                        else:
                            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
                        try:
                            cursor.execute("DELETE FROM interactions_app_interestrequest WHERE sender_id = %s OR receiver_id = %s", [user.id, user.id])
                        except Exception:
                            pass
                        try:
                            cursor.execute("DELETE FROM profiles_app_profile WHERE id = %s", [profile_id])
                        except Exception:
                            pass
                        try:
                            cursor.execute("DELETE FROM auth_user WHERE id = %s", [user.id])
                        except Exception:
                            pass
                        if connection.vendor == 'sqlite':
                            cursor.execute("PRAGMA foreign_keys = ON;")
                        else:
                            cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
            else:
                try:
                    from django.db import connection
                    with connection.cursor() as cursor:
                        if connection.vendor == 'sqlite':
                            cursor.execute("PRAGMA foreign_keys = OFF;")
                        else:
                            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
                        cursor.execute("DELETE FROM profiles_app_profile WHERE id = %s", [profile_id])
                        if connection.vendor == 'sqlite':
                            cursor.execute("PRAGMA foreign_keys = ON;")
                        else:
                            cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
                except Exception:
                    pass
                
            return JsonResponse({'status': 'success', 'message': 'User deleted completely.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)


# ==========================================
# OMKAR - AUTHENTICATION MODULE (ADMIN VIEWS)
# ==========================================
from django.contrib.auth.models import User
from django.db.models import Q

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def auth_users(request):
    """View to manage all registered users."""
    q = request.GET.get('q', '')
    users = User.objects.exclude(profile__gender__isnull=True).exclude(profile__gender__exact='').order_by('-date_joined')
    
    if q:
        users = users.filter(
            Q(username__icontains=q) | 
            Q(email__icontains=q) | 
            Q(first_name__icontains=q) | 
            Q(last_name__icontains=q)
        )
        
    context = {'users': users, 'search_query': q}
    return render(request, 'admin_panel/auth_users.html', context)

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def auth_login_logs(request):
    """View to track recent logins (using last_login as proxy)."""
    users = User.objects.exclude(last_login__isnull=True).order_by('-last_login')[:50]
    context = {'users': users}
    return render(request, 'admin_panel/auth_login_logs.html', context)

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def auth_security(request):
    # Also acting as Platform Settings
    settings = PlatformSetting.objects.all()
    if not settings.filter(key='Maintenance Mode').exists():
        PlatformSetting.objects.create(key='Maintenance Mode', value='False', description='Disable user logins')
    if not settings.filter(key='Auto-Approve Photos').exists():
        PlatformSetting.objects.create(key='Auto-Approve Photos', value='True', description='Approve photos automatically')
        
    # Only show settings that are meant to be ON/OFF toggles
    toggle_settings = PlatformSetting.objects.filter(key__in=['Maintenance Mode', 'Auto-Approve Photos'])
    
    return render(request, 'admin_panel/platform_settings.html', {'settings': toggle_settings})

@csrf_exempt
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def toggle_setting(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            setting_id = data.get('setting_id')
            setting = PlatformSetting.objects.get(id=setting_id)
            setting.value = 'False' if setting.value == 'True' else 'True'
            setting.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def auth_roles(request):
    """View to manage Roles (Admin, Staff, Normal)."""
    admins = User.objects.filter(is_superuser=True)
    staff = User.objects.filter(is_staff=True, is_superuser=False)
    users = User.objects.filter(is_staff=False, is_superuser=False)
    
    context = {
        'admins': admins,
        'staff': staff,
        'users': users
    }
    return render(request, 'admin_panel/auth_roles.html', context)

@csrf_exempt
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def update_user_role(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            new_role = data.get('role')
            
            from django.contrib.auth.models import User
            user = User.objects.get(id=user_id)
            
            if new_role == 'admin':
                user.is_superuser = True
                user.is_staff = True
            elif new_role == 'staff':
                user.is_superuser = False
                user.is_staff = True
            else:
                user.is_superuser = False
                user.is_staff = False
            
            user.save()
            return JsonResponse({'status': 'success', 'message': 'Role updated successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)


from profiles_app.models import Profile

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def gauri_manage_profiles(request):
    profiles = Profile.objects.select_related('user').filter(user__is_superuser=False, user__is_staff=False).order_by('-created_at')
    return render(request, 'admin_panel/gauri_manage_profiles.html', {'profiles': profiles})

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def gauri_photo_approvals(request):
    profiles = Profile.objects.exclude(photo='').exclude(photo__isnull=True).filter(is_photo_approved=False).order_by('-created_at')
    return render(request, 'admin_panel/gauri_photo_approvals.html', {'profiles': profiles})

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def gauri_partner_preferences(request):
    profiles = Profile.objects.select_related('user').filter(user__is_superuser=False, user__is_staff=False).order_by('-created_at')
    return render(request, 'admin_panel/gauri_partner_preferences.html', {'profiles': profiles})


@csrf_exempt
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def approve_photo(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        profile_id = data.get('profile_id')
        try:
            profile = Profile.objects.get(id=profile_id)
            profile.is_photo_approved = True
            profile.save()
            return JsonResponse({'status': 'success'})
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Profile not found'}, status=404)
    return JsonResponse({'status': 'error'}, status=405)

@csrf_exempt
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def reject_photo(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        profile_id = data.get('profile_id')
        try:
            profile = Profile.objects.get(id=profile_id)
            profile.photo = None
            profile.is_photo_approved = False
            profile.save()
            return JsonResponse({'status': 'success'})
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Profile not found'}, status=404)
    return JsonResponse({'status': 'error'}, status=405)


from interactions_app.models import InterestRequest

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def sandhya_match_search(request):
    # Admin view to search across all profiles
    profiles = Profile.objects.select_related('user').filter(user__is_superuser=False, user__is_staff=False).order_by('-created_at')
    
    query = request.GET.get('q')
    if query:
        profiles = profiles.filter(
            Q(user__username__icontains=query) |
            Q(full_name__icontains=query) |
            Q(city__icontains=query)
        )
        
    return render(request, 'admin_panel/sandhya_match_search.html', {'profiles': profiles, 'query': query})

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def sandhya_pending_requests(request):
    # View all interest requests happening on the platform
    interests = InterestRequest.objects.all().select_related('sender__profile', 'receiver__profile').order_by('-created_at')
    
    return render(request, 'admin_panel/sandhya_pending_requests.html', {'interests': interests})

@csrf_exempt
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def toggle_user_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            user = User.objects.get(id=user_id)
            # Cannot ban superusers
            if user.is_superuser:
                return JsonResponse({'status': 'error', 'message': 'Cannot ban superusers.'}, status=400)
            
            user.is_active = not user.is_active
            user.save()
            action = "Activated" if user.is_active else "Banned"
            return JsonResponse({'status': 'success', 'message': f'User {action} successfully.'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def revenue_reports(request):
    from payments_app.models import Transaction
    from django.db.models import Sum
    from django.utils import timezone

    # Total Revenue
    total_rev = Transaction.objects.filter(status='Success').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # This Month Revenue
    now = timezone.now()
    this_month_rev = Transaction.objects.filter(
        status='Success', 
        timestamp__year=now.year, 
        timestamp__month=now.month
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Active Subscriptions
    active_subs = Transaction.objects.filter(status='Success').count()

    context = {
        'total_revenue': total_rev,
        'this_month': this_month_rev,
        'active_subscriptions': active_subs
    }
    return render(request, 'admin_panel/revenue_reports.html', context)

from .models import SuccessStory, PlatformSetting
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def success_stories(request):
    stories = SuccessStory.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/success_stories.html', {'stories': stories})

@csrf_exempt
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def toggle_story_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            story_id = data.get('story_id')
            story = SuccessStory.objects.get(id=story_id)
            story.is_approved = not story.is_approved
            story.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)

# ==========================================
# MUKTA - PAYMENTS MODULE (ADMIN VIEWS)
# ==========================================
from payments_app.models import MembershipPlan, Transaction

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def mukta_memberships(request):
    plans = MembershipPlan.objects.all().order_by('price')
    return render(request, 'admin_panel/mukta_memberships.html', {'plans': plans})

@csrf_exempt
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def save_plan(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        plan_id = data.get('id')
        name = data.get('name')
        price = data.get('price')
        duration = data.get('duration_months')
        features = data.get('features')

        if plan_id:
            try:
                plan = MembershipPlan.objects.get(id=plan_id)
                plan.name = name
                plan.price = price
                plan.duration_months = duration
                plan.features = features
                plan.save()
                return JsonResponse({'status': 'success', 'message': 'Plan updated successfully'})
            except MembershipPlan.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Plan not found'})
        else:
            MembershipPlan.objects.create(name=name, price=price, duration_months=duration, features=features)
            return JsonResponse({'status': 'success', 'message': 'Plan added successfully'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@csrf_exempt
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def toggle_plan_status(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        plan_id = data.get('id')
        try:
            plan = MembershipPlan.objects.get(id=plan_id)
            plan.is_active = not plan.is_active
            plan.save()
            return JsonResponse({'status': 'success'})
        except MembershipPlan.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Plan not found'})
    return JsonResponse({'status': 'error'})

@csrf_exempt
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def delete_plan(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        plan_id = data.get('id')
        try:
            plan = MembershipPlan.objects.get(id=plan_id)
            plan.delete()
            return JsonResponse({'status': 'success'})
        except MembershipPlan.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Plan not found'})
    return JsonResponse({'status': 'error'})

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def mukta_billing(request):
    transactions = Transaction.objects.all().order_by('-timestamp')
    return render(request, 'admin_panel/mukta_billing.html', {'transactions': transactions})

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def mukta_gateway(request):
    from admin_panel.models import PlatformSetting
    # Fetch real keys from DB, or fallback to test keys if empty
    key_id_obj, _ = PlatformSetting.objects.get_or_create(key='razorpay_key_id', defaults={'value': 'rzp_test_TGDV3MhXpMq92X'})
    key_secret_obj, _ = PlatformSetting.objects.get_or_create(key='razorpay_key_secret', defaults={'value': 'hHN0McnuOUGvu7B2gv399vY4'})
    
    context = {
        'razorpay_key_id': key_id_obj.value,
        'razorpay_key_secret': key_secret_obj.value
    }
    return render(request, 'admin_panel/mukta_gateway.html', context)

@csrf_exempt
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def save_payment_gateway(request):
    """Secure endpoint to update Razorpay keys"""
    if request.method == 'POST':
        try:
            from admin_panel.models import PlatformSetting
            data = json.loads(request.body)
            key_id = data.get('razorpay_key_id')
            key_secret = data.get('razorpay_key_secret')
            
            key_id_obj, _ = PlatformSetting.objects.get_or_create(key='razorpay_key_id')
            key_id_obj.value = key_id
            key_id_obj.save()
            
            key_secret_obj, _ = PlatformSetting.objects.get_or_create(key='razorpay_key_secret')
            key_secret_obj.value = key_secret
            key_secret_obj.save()
            
            return JsonResponse({'status': 'success', 'message': 'Payment Gateway keys updated successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

# ==========================================
# 6. SARTHAK'S MODULE: FRONTEND & WEB
# ==========================================

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def sarthak_website_content(request):
    from admin_panel.models import PlatformSetting
    
    # Get or create dynamic content
    heading, _ = PlatformSetting.objects.get_or_create(key='website_heading', defaults={'value': 'Welcome to ForeverBond'})
    desc, _ = PlatformSetting.objects.get_or_create(key='website_description', defaults={'value': 'We help millions of people find their perfect match across the globe. Our advanced AI algorithms ensure that you only meet verified and compatible partners.'})
    privacy, _ = PlatformSetting.objects.get_or_create(key='privacy_policy_url', defaults={'value': '/privacy-policy/'})
    terms, _ = PlatformSetting.objects.get_or_create(key='terms_url', defaults={'value': '/terms-and-conditions/'})
    
    context = {
        'website_heading': heading.value,
        'website_description': desc.value,
        'privacy_policy_url': privacy.value,
        'terms_url': terms.value,
    }
    return render(request, 'admin_panel/sarthak_website_content.html', context)

@csrf_exempt
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def save_website_content(request):
    if request.method == 'POST':
        try:
            from admin_panel.models import PlatformSetting
            data = json.loads(request.body)
            
            heading, _ = PlatformSetting.objects.get_or_create(key='website_heading')
            heading.value = data.get('website_heading', '')
            heading.save()
            
            desc, _ = PlatformSetting.objects.get_or_create(key='website_description')
            desc.value = data.get('website_description', '')
            desc.save()
            
            privacy, _ = PlatformSetting.objects.get_or_create(key='privacy_policy_url')
            privacy.value = data.get('privacy_policy_url', '')
            privacy.save()
            
            terms, _ = PlatformSetting.objects.get_or_create(key='terms_url')
            terms.value = data.get('terms_url', '')
            terms.save()
            
            return JsonResponse({'status': 'success', 'message': 'Website content updated successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def sarthak_chat_logs(request):
    """
    Admin view to monitor chat logs.
    """
    try:
        from interactions_app.models import ChatMessage
        messages = ChatMessage.objects.all().order_by('-timestamp')
    except Exception:
        messages = []
        
    context = {
        'messages': messages
    }
    return render(request, 'admin_panel/sarthak_chat_logs.html', context)

# ==========================================
# 7. NEW FEATURES: MASTER DATA, KYC, REPORTS
# ==========================================

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def manage_master_data(request):
    """View to manage Religion, Caste, and Mother Tongue master data"""
    from profiles_app.models import Religion, Caste, MotherTongue
    
    if request.method == 'POST':
        # Simple handler to add new items
        action = request.POST.get('action')
        name = request.POST.get('name')
        if action == 'add_religion' and name:
            Religion.objects.get_or_create(name=name.strip())
        elif action == 'add_caste' and name:
            rel_id = request.POST.get('religion_id')
            if rel_id:
                rel = Religion.objects.get(id=rel_id)
                Caste.objects.get_or_create(religion=rel, name=name.strip())
        elif action == 'add_tongue' and name:
            MotherTongue.objects.get_or_create(name=name.strip())
            
        elif action == 'delete_religion':
            item_id = request.POST.get('item_id')
            if item_id: Religion.objects.filter(id=item_id).delete()
        elif action == 'delete_caste':
            item_id = request.POST.get('item_id')
            if item_id: Caste.objects.filter(id=item_id).delete()
        elif action == 'delete_tongue':
            item_id = request.POST.get('item_id')
            if item_id: MotherTongue.objects.filter(id=item_id).delete()
            
        return redirect('manage_master_data')
        
    context = {
        'religions': Religion.objects.all().order_by('name'),
        'castes': Caste.objects.select_related('religion').all().order_by('religion__name', 'name'),
        'tongues': MotherTongue.objects.all().order_by('name')
    }
    return render(request, 'admin_panel/manage_master_data.html', context)

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def kyc_approvals(request):
    """View to manage ID Proof verifications"""
    from profiles_app.models import KYCDocument
    
    if request.method == 'POST':
        doc_id = request.POST.get('doc_id')
        action = request.POST.get('action')
        if doc_id and action in ['Approve', 'Reject']:
            try:
                doc = KYCDocument.objects.get(id=doc_id)
                doc.status = 'Approved' if action == 'Approve' else 'Rejected'
                doc.save()
            except KYCDocument.DoesNotExist:
                pass
        return redirect('kyc_approvals')

    pending_docs = KYCDocument.objects.filter(status='Pending').select_related('user').order_by('-submitted_at')
    history_docs = KYCDocument.objects.exclude(status='Pending').select_related('user').order_by('-submitted_at')[:50]
    
    context = {
        'pending_docs': pending_docs,
        'history_docs': history_docs
    }
    return render(request, 'admin_panel/kyc_approvals.html', context)

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def reported_profiles(request):
    """View to manage user reports/complaints"""
    from interactions_app.models import Report
    from django.contrib.auth.models import User
    
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        action = request.POST.get('action')
        
        try:
            report = Report.objects.get(id=report_id)
            if action == 'resolve':
                report.is_resolved = True
                report.save()
            elif action == 'ban':
                user_to_ban = report.reported_user
                user_to_ban.is_active = False
                user_to_ban.save()
                report.is_resolved = True
                report.save()
        except Report.DoesNotExist:
            pass
            
        return redirect('reported_profiles')

    pending_reports = Report.objects.filter(is_resolved=False).select_related('reporter', 'reported_user').order_by('-timestamp')
    resolved_reports = Report.objects.filter(is_resolved=True).select_related('reporter', 'reported_user').order_by('-timestamp')[:50]
    
    context = {
        'pending_reports': pending_reports,
        'resolved_reports': resolved_reports
    }
    return render(request, 'admin_panel/reported_profiles.html', context)

from django.shortcuts import get_object_or_404
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def admin_view_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    gallery = profile.gallery_photos.all()
    gallery_count = gallery.count()
    return render(request, 'admin_panel/admin_view_profile.html', {
        'profile': profile,
        'gallery': gallery,
        'gallery_count': gallery_count
    })

import csv
from django.http import HttpResponse

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def export_billing_csv(request):
    from payments_app.models import Transaction
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="billing_transactions.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'Amount (Rs)', 'Plan Name', 'Status', 'Date & Time', 'Order ID', 'Payment ID'])
    
    transactions = Transaction.objects.all().order_by('-timestamp').select_related('user', 'plan')
    
    from django.utils.timezone import localtime
    
    for txn in transactions:
        if txn.timestamp:
            try:
                dt_str = localtime(txn.timestamp).strftime("%d-%m-%Y %I:%M %p")
            except:
                dt_str = txn.timestamp.strftime("%d-%m-%Y %I:%M %p")
        else:
            dt_str = "N/A"
            
        writer.writerow([
            txn.user.username,
            txn.user.email,
            txn.amount,
            txn.plan.name if txn.plan else "N/A",
            txn.status,
            dt_str,
            txn.razorpay_order_id,
            txn.razorpay_payment_id
        ])
        
    return response

from django.core.mail import send_mail
from django.conf import settings
from website.models import CounselingQuery
from django.contrib import messages
from django.shortcuts import redirect, render

@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.is_staff), login_url="/admin_panel/login/")
def counseling_queries(request):
    
    if request.method == 'POST':
        query_id = request.POST.get('query_id')
        reply_text = request.POST.get('reply_text')
        
        if query_id and reply_text:
            query = CounselingQuery.objects.get(id=query_id)
            query.admin_reply = reply_text
            query.is_resolved = True
            query.save()
            
            subject = f"Re: Your Counseling Query about {query.topic}"
            message = f"Dear {query.full_name},\n\nThank you for reaching out to us regarding '{query.topic}'.\n\nCounselor's Reply:\n{query.admin_reply}\n\nBest regards,\nForeverBond Counseling Team"
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [query.email], fail_silently=False)
                messages.success(request, "Reply sent successfully!")
            except Exception as e:
                messages.error(request, f"Failed to send email: {e}")
                
            return redirect('counseling_queries')
            
    queries = CounselingQuery.objects.all().order_by('-submitted_at')
    return render(request, 'admin_panel/counseling_queries.html', {'queries': queries})
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

def contact_queries(request):
    from .models import ContactMessage
    if request.method == 'POST':
        query_id = request.POST.get('query_id')
        reply_text = request.POST.get('reply_text')
        try:
            msg = ContactMessage.objects.get(id=query_id)
            msg.is_resolved = True
            msg.save()
            
            if reply_text and reply_text.strip():
                # Send reply email
                send_mail(
                    f"Re: {msg.subject}",
                    f"Dear {msg.name},\n\n{reply_text}\n\nBest Regards,\nSoulMate Matrimony Team",
                    settings.EMAIL_HOST_USER,
                    [msg.email],
                    fail_silently=False,
                )
                messages.success(request, f"Reply sent to {msg.name} and query marked as resolved.")
            else:
                messages.success(request, f"Query from {msg.name} marked as resolved without email reply.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        return redirect('contact_queries')
        
    queries = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/contact_queries.html', {'queries': queries})

from django.http import JsonResponse
def toggle_contact_status(request):
    if request.method == 'POST':
        from .models import ContactMessage
        import json
        data = json.loads(request.body)
        msg_id = data.get('id')
        try:
            msg = ContactMessage.objects.get(id=msg_id)
            msg.is_resolved = not msg.is_resolved
            msg.save()
            return JsonResponse({'status': 'success', 'is_resolved': msg.is_resolved})
        except ContactMessage.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Message not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

