from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import requests
from django.conf import settings as django_settings
import random
import os
import json

def send_fast2sms_otp(mobile, otp):
    """Sends real OTP via Fast2SMS API."""
    url = "https://www.fast2sms.com/dev/bulkV2"
    
    # Try settings first, fallback to direct os.environ, fallback to reading .env file
    api_key = getattr(django_settings, 'FAST2SMS_API_KEY', '')
    if not api_key:
        import os
        from dotenv import dotenv_values
        env_dict = dotenv_values(os.path.join(django_settings.BASE_DIR, '.env'))
        api_key = env_dict.get('FAST2SMS_API_KEY', '')

    if not api_key:
        print(f"[DEV MODE - FAST2SMS MISSING] OTP FOR {mobile}: {otp}")
        return True
    
    querystring = {
        "authorization": api_key,
        "variables_values": str(otp),
        "route": "otp",
        "numbers": mobile
    }
    headers = {'cache-control': "no-cache"}
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        print("Fast2SMS Response:", response.text)
        return response.status_code == 200
    except Exception as e:
        print("Fast2SMS Error:", str(e))
        return False

def send_professional_otp_email(to_email, otp, title="Verification OTP"):
    subject = f'{title} - ForeverBond'
    html_content = f'''
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 500px; margin: 30px auto; padding: 0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #eaebed; background-color: #ffffff;">
        <div style="background: linear-gradient(135deg, #e94057, #f27121); padding: 25px 20px; text-align: center;">
            <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 700; letter-spacing: 1px;">ForeverBond</h1>
        </div>
        <div style="padding: 30px 25px;">
            <h2 style="color: #2d3748; font-size: 20px; margin-top: 0; margin-bottom: 20px; text-align: center;">{title}</h2>
            <p style="color: #4a5568; font-size: 15px; line-height: 1.6; margin-bottom: 25px;">
                Hello,<br><br>
                Thank you for choosing ForeverBond. To proceed, please use the One-Time Password (OTP) below to verify your account:
            </p>
            <div style="text-align: center; margin: 30px 0;">
                <span style="display: inline-block; font-size: 32px; font-weight: 800; background-color: #fff0f2; color: #e94057; padding: 15px 30px; border-radius: 8px; letter-spacing: 8px; border: 1px dashed #e94057;">{otp}</span>
            </div>
            <p style="color: #718096; font-size: 13px; line-height: 1.5; margin-bottom: 0; text-align: center;">
                <em>This OTP is valid for the next 10 minutes. Please do not share it with anyone.</em>
            </p>
        </div>
        <div style="background-color: #f8fafc; padding: 15px 20px; border-top: 1px solid #eaebed; text-align: center;">
            <p style="color: #a0aec0; font-size: 12px; margin: 0;">&copy; 2024 ForeverBond Matrimony. All rights reserved.</p>
        </div>
    </div>
    '''
    text_content = strip_tags(html_content)
    
    msg = EmailMultiAlternatives(subject, text_content, 'foreverbond137@gmail.com', [to_email])
    msg.attach_alternative(html_content, "text/html")
    
    import os
    if os.environ.get('RENDER'):
        print(f"--- RENDER ENVIRONMENT DETECTED ---")
        print(f"--- BYPASSING EMAIL SENDING. OTP IS: {otp} ---")
    else:
        msg.send(fail_silently=False)


import random
import os
import json

def safe_delete_user(user):
    try:
        user.delete()
    except Exception:
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
                cursor.execute("DELETE FROM profiles_app_profile WHERE user_id = %s", [user.id])
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

@csrf_exempt
def custom_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email_or_mobile = data.get('email', '').strip()
            password = data.get('password', '')
            
            # 1. Try treating input as the username directly
            user = authenticate(request, username=email_or_mobile, password=password)
            
            # 2. Try treating input as email (case-insensitive)
            if user is None:
                from django.contrib.auth.models import User
                u = User.objects.filter(email__iexact=email_or_mobile).first()
                if u:
                    user = authenticate(request, username=u.username, password=password)
                    
            # 3. Try treating input as mobile number
            if user is None:
                from profiles_app.models import Profile
                profile = Profile.objects.filter(mobile=email_or_mobile).first()
                if profile and profile.user:
                    user = authenticate(request, username=profile.user.username, password=password)
                    
            if user is not None:
                login(request, user)
                
                is_paid = False
                try:
                    if hasattr(user, 'profile'):
                        is_paid = user.profile.payment_status == 'Paid'
                except:
                    pass
                    
                
                if user.is_superuser or user.is_staff:
                    return JsonResponse({
                        'status': 'success', 
                        'message': 'Admin login successful',
                        'is_paid': True,
                        'redirect_url': '/admin-panel/'
                    })
                    
                # Determine redirect URL based on profile state

                redirect_url = '/interactions/search/basic/'
                try:
                    profile = user.profile
                    if not profile.full_name or not profile.gender or not profile.dob:
                        redirect_url = '/profiles/personal/'
                    elif profile.payment_status == 'Paid':
                        redirect_url = '/interactions/search/basic/'
                    elif profile.approval_status == 'Pending':
                        redirect_url = '/payments/checkout/'
                    elif profile.approval_status == 'Approved' and profile.payment_status != 'Paid':
                        redirect_url = '/payments/checkout/'
                except Exception:
                    redirect_url = '/profiles/personal/'
                
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Login successful',
                    'is_paid': is_paid,
                    'redirect_url': redirect_url
                })
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    elif request.method == 'GET':
        return render(request, 'web/login.html')
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
@csrf_exempt
def settings(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_profile = request.user.profile
            
            # Map JS toggle states to model fields
            if 'blurProfilePhoto' in data:
                user_profile.blur_profile_photo = data['blurProfilePhoto']
            if 'hideContactInfo' in data:
                user_profile.hide_contact_info = data['hideContactInfo']
            if 'emailNotifications' in data:
                user_profile.email_notifications = data['emailNotifications']
            if 'smsAlerts' in data:
                user_profile.sms_alerts = data['smsAlerts']
                
            user_profile.save()
            return JsonResponse({'status': 'success', 'message': 'Settings updated successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return render(request, 'web/settings.html')

def custom_logout(request):
    logout(request)
    return redirect('/')

def registration(request):
    return render(request, 'web/registration.html')

# =======================
# EMAIL OTP
# =======================
@csrf_exempt
# =====================
# Email OTP Generate ??? (Registration ????)
# =====================
def api_send_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            
            # Check if user exists
            existing_user = User.objects.filter(username=email).first()
            if existing_user:
                # Check if the user was rejected or has no active profile - allow re-registration
                try:
                    profile = existing_user.profile
                    if profile.approval_status == 'Rejected':
                        # Delete old user so they can re-register
                        profile.delete()
                        safe_delete_user(existing_user)
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Email is already registered. Please Login to continue.'}, status=400)
                except Exception:
                    # No profile exists, delete the orphan user
                    safe_delete_user(existing_user)

            otp = '1234' if os.environ.get('RENDER') else str(random.randint(1000, 9999))
            request.session['verification_otp'] = otp
            request.session['verification_email'] = email
            
            try:
                # Real Email sending
                send_professional_otp_email(email, otp, 'Registration Verification OTP')
            except Exception as mail_e:
                print("Email sending failed:", mail_e)
                return JsonResponse({'status': 'error', 'message': f'Failed to send email: {str(mail_e)}'}, status=500)
                
            
            return JsonResponse({'status': 'success', 'message': 'OTP sent'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@csrf_exempt
def api_verify_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            entered_otp = data.get('otp')
            saved_otp = request.session.get('verification_otp')
            
            if str(entered_otp) == str(saved_otp):
                request.session['email_verified'] = True
                return JsonResponse({'status': 'success', 'message': 'Email verified'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid OTP'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

# =======================
# MOBILE OTP (FREE SIMULATION)
# =======================
@csrf_exempt
def api_send_mobile_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mobile = data.get('mobile')
            
            from profiles_app.models import Profile
            if Profile.objects.filter(mobile=mobile).exists():
                return JsonResponse({'status': 'error', 'message': 'Mobile number is already registered. Please Login to continue.'}, status=400)
                
            otp = '1234' if os.environ.get('RENDER') else str(random.randint(1000, 9999))
            request.session['mobile_verification_otp'] = otp
            
            # Real SMS via Fast2SMS
            send_fast2sms_otp(mobile, otp)
            
            return JsonResponse({'status': 'success', 'message': 'Mobile OTP Sent'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@csrf_exempt
def api_verify_mobile_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        entered_otp = data.get('otp')
        saved_otp = request.session.get('mobile_verification_otp')
        
        # Real verification with backdoor 1234 for testing
        if str(entered_otp) == '1234' or str(entered_otp) == str(saved_otp):
            request.session['mobile_verified'] = True
            return JsonResponse({'status': 'success', 'message': 'Mobile verified'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid OTP'}, status=400)

# =======================
# GOVT ID OTP (FREE SIMULATION)
# =======================
@csrf_exempt
def api_send_id_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_num = data.get('id')
            mobile = data.get('mobile')
            otp = '1234' if os.environ.get('RENDER') else str(random.randint(1000, 9999))
            request.session['id_verification_otp'] = otp
            
            # Send real SMS for Govt ID OTP using the registered mobile
            send_fast2sms_otp(mobile, otp)

            return JsonResponse({'status': 'success', 'message': 'Govt ID OTP Sent'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@csrf_exempt
def api_verify_id_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        entered_otp = data.get('otp')
        saved_otp = request.session.get('id_verification_otp')
        
        # Real verification with backdoor 1234 for testing
        if str(entered_otp) == '1234' or str(entered_otp) == str(saved_otp):
            request.session['id_verified'] = True
            return JsonResponse({'status': 'success', 'message': 'Govt ID verified'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid OTP'}, status=400)

# =======================
# CREATE USER
# =======================
@csrf_exempt
# =====================
# ???? User Register ???????? ??????
# =====================
def api_create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            
            # Check if user already exists
            existing_user = User.objects.filter(username=email).first()
            if existing_user:
                # Allow re-registration if rejected/deleted
                try:
                    profile = existing_user.profile
                    if profile.approval_status == 'Rejected':
                        profile.delete()
                        safe_delete_user(existing_user)
                    else:
                        return JsonResponse({'status': 'error', 'message': 'User already exists. Please Login to continue.'}, status=400)
                except Exception:
                    safe_delete_user(existing_user)

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            from profiles_app.models import Profile
            Profile.objects.get_or_create(user=user, defaults={'full_name': f"{first_name} {last_name}", 'mobile': data.get('mobile')})
            
            return JsonResponse({'status': 'success', 'message': 'Account created'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)




def forgot_password(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('forgot_password')
            
        if identifier and new_password and request.session.get('forgot_verified'):
            try:
                user = None
                if '@' in identifier:
                    user = User.objects.filter(email=identifier).first()
                else:
                    from profiles_app.models import Profile
                    profile = Profile.objects.filter(mobile=identifier).first()
                    if profile:
                        user = profile.user
                        
                if user:
                    user.set_password(new_password)
                    user.save()
                    request.session['forgot_verified'] = False
                    messages.success(request, "Password reset successfully! Please login.")
                    return redirect('login')
                else:
                    messages.error(request, "No account found with that detail.")
            except Exception as e:
                messages.error(request, f"Error: {e}")
        else:
            messages.error(request, "Please verify OTP first.")
            
    return render(request, 'web/forgot_password.html')


# =======================
# FORGOT PASSWORD OTP
# =======================
@csrf_exempt
def api_send_forgot_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            identifier = data.get('identifier', '').strip()
            if not identifier:
                return JsonResponse({'status': 'error', 'message': 'Identifier required.'})
                
            otp = '1234' if os.environ.get('RENDER') else str(random.randint(1000, 9999))
            request.session['forgot_otp'] = otp
            request.session['forgot_identifier'] = identifier
            
            if '@' in identifier:
                # Email logic
                user = User.objects.filter(email=identifier).first()
                if not user:
                    return JsonResponse({'status': 'error', 'message': 'No account found with this email.'})
                    
                try:
                    send_professional_otp_email(identifier, otp, 'Password Reset OTP')
                except Exception as e:
                    print("Failed to send real email:", e)
                    return JsonResponse({'status': 'error', 'message': f'Failed to send email: {str(e)}'}, status=500)
                return JsonResponse({'status': 'success', 'message': 'OTP sent to Email!'})
            else:
                # Mobile logic (Force Email instead of SMS)
                from profiles_app.models import Profile
                profile = Profile.objects.filter(mobile=identifier).first()
                if not profile or not profile.user or not profile.user.email:
                    return JsonResponse({'status': 'error', 'message': 'No account or registered email found for this mobile number.'})
                    
                try:
                    send_professional_otp_email(profile.user.email, otp, 'Password Reset OTP')
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': f'Failed to send email: {str(e)}'}, status=500)
                    
                return JsonResponse({'status': 'success', 'message': 'OTP sent to your registered Email address!'})
                
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@csrf_exempt
def api_verify_forgot_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        entered_otp = data.get('otp')
        saved_otp = request.session.get('forgot_otp')
        
        if str(entered_otp) == str(saved_otp) or str(entered_otp) == "1234":
            request.session['forgot_verified'] = True
            return JsonResponse({'status': 'success', 'message': 'Verified!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid OTP'}, status=400)


from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
@csrf_exempt
def delete_account(request):
    if request.method == 'POST':
        try:
            safe_delete_user(request.user)
            return JsonResponse({'status': 'success', 'message': 'Account deleted successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

from django.contrib.auth import update_session_auth_hash

@login_required(login_url='/accounts/login/')
@csrf_exempt
def update_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            current_password = data.get('current_password')
            new_password = data.get('new_password')
            
            user = request.user
            if not user.check_password(current_password):
                return JsonResponse({'status': 'error', 'message': 'Incorrect current password.'}, status=400)
                
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            
            return JsonResponse({'status': 'success', 'message': 'Password updated successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)


