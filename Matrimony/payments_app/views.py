import json
import razorpay
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from profiles_app.models import Profile

# --- RAZORPAY SETTINGS (Dynamic from DB) ---
def get_razorpay_keys():
    try:
        from admin_panel.models import PlatformSetting
        key_id = PlatformSetting.objects.get(key='razorpay_key_id').value
        key_secret = PlatformSetting.objects.get(key='razorpay_key_secret').value
        if key_id and key_secret:
            return key_id, key_secret
    except Exception:
        pass
    return "rzp_test_TGDV3MhXpMq92X", "hHN0McnuOUGvu7B2gv399vY4"
# ------------------------------------------------------------------

@login_required(login_url='/accounts/login/')
def checkout(request):
    """
    Renders the Packages/Checkout page.
    Passes the Razorpay Key ID to the frontend.
    """
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
        
    plan_id = request.GET.get('plan')
    plan = None
    if plan_id:
        from .models import MembershipPlan
        plan = MembershipPlan.objects.filter(id=plan_id).first()
        if plan:
            request.session['selected_plan_id'] = plan.id
            
    razorpay_key_id, _ = get_razorpay_keys()
    context = {
        'razorpay_key_id': razorpay_key_id,
        'plan': plan
    }
    return render(request, 'web/checkout.html', context)

@csrf_exempt
def create_order(request):
    """
    Creates a Razorpay order from the backend.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=403)
        
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount_in_rupees = int(data.get('amount', 0))
            amount_in_paise = amount_in_rupees * 100
            
            # Note: Since we are using dummy keys, real Razorpay client will throw Unauthorized error.
            # To prevent crash while testing without keys, we catch it.
            try:
                razorpay_key_id, razorpay_key_secret = get_razorpay_keys()
                client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))
                order_data = {
                    'amount': amount_in_paise,
                    'currency': 'INR',
                    'payment_capture': 1
                }
                order = client.order.create(data=order_data)
                order_id = order.get('id')
            except Exception as e:
                # Fallback to mock order if Razorpay fails (due to dummy keys)
                print("Razorpay API Error (Probably using dummy keys):", str(e))
                order_id = "order_mock_" + str(amount_in_paise)
                
            return JsonResponse({
                'status': 'success',
                'order_id': order_id,
                'amount': amount_in_paise
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@csrf_exempt
def verify_payment(request):
    """
    Verifies the payment signature and unlocks the profile.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=403)
        
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            payment_id = data.get('razorpay_payment_id', '')
            order_id = data.get('razorpay_order_id', '')
            signature = data.get('razorpay_signature', '')
            
            # Verify Signature using Razorpay SDK
            # If using mock order, we bypass verification
            if not order_id.startswith('order_mock_'):
                razorpay_key_id, razorpay_key_secret = get_razorpay_keys()
                client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))
                params_dict = {
                    'razorpay_order_id': order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': signature
                }
                # Throws SignatureVerificationError if invalid
                client.utility.verify_payment_signature(params_dict)

            # Log Transaction first to get plan
            selected_plan_id = request.session.get('selected_plan_id')
            plan = None
            if selected_plan_id:
                from .models import MembershipPlan
                plan = MembershipPlan.objects.filter(id=selected_plan_id).first()

            # Verification successful, update profile
            profile = Profile.objects.get(user=request.user)
            profile.payment_status = 'Paid'
            
            if plan:
                from datetime import timedelta
                from django.utils import timezone
                profile.active_plan = plan
                profile.plan_expiry_date = timezone.now() + timedelta(days=plan.duration_months * 30)
                
            profile.save()
                
            from .models import Transaction
            Transaction.objects.create(
                user=request.user,
                plan=plan,
                amount=plan.price if plan else 999,
                status='Success',
                razorpay_order_id=order_id,
                razorpay_payment_id=payment_id
            )
            
            return JsonResponse({'status': 'success', 'message': 'Payment successful!'})
            
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({'status': 'error', 'message': 'Invalid payment signature!'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)


def pay_link(request, user_id):
    """
    External payment link sent by admin.
    """
    from .models import MembershipPlan
    plans = MembershipPlan.objects.filter(is_active=True).order_by('price')
    razorpay_key_id, _ = get_razorpay_keys()
    return render(request, 'web/external_payment_link.html', {
        'target_user_id': user_id,
        'plans': plans,
        'razorpay_key_id': razorpay_key_id
    })

@csrf_exempt
def create_external_order(request, user_id):
    """
    Creates a Razorpay order from the external payment link (without login).
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount_in_rupees = int(data.get('amount', 0))
            amount_in_paise = amount_in_rupees * 100
            
            try:
                razorpay_key_id, razorpay_key_secret = get_razorpay_keys()
                client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))
                order_data = {
                    'amount': amount_in_paise,
                    'currency': 'INR',
                    'payment_capture': 1
                }
                order = client.order.create(data=order_data)
                order_id = order.get('id')
            except Exception as e:
                print("Razorpay API Error (Probably using dummy keys):", str(e))
                order_id = "order_mock_" + str(amount_in_paise)
                
            return JsonResponse({
                'status': 'success',
                'order_id': order_id,
                'amount': amount_in_paise
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

import json
from .models import MembershipPlan, Transaction

@csrf_exempt
def verify_payment_link(request, user_id):
    """
    Verifies payment from the external link and records a Transaction.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            plan_id = data.get('plan_id')
            payment_id = data.get('razorpay_payment_id', '')
            order_id = data.get('razorpay_order_id', '')
            signature = data.get('razorpay_signature', '')
            
            if not order_id.startswith('order_mock_'):
                razorpay_key_id, razorpay_key_secret = get_razorpay_keys()
                client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))
                params_dict = {
                    'razorpay_order_id': order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': signature
                }
                client.utility.verify_payment_signature(params_dict)

            profile = Profile.objects.get(user__id=user_id)
            
            plan = None
            amount = 0
            if plan_id:
                plan = MembershipPlan.objects.filter(id=plan_id).first()
                if plan:
                    amount = plan.price
            
            Transaction.objects.create(
                user=profile.user,
                plan=plan,
                amount=amount,
                status='Success',
                razorpay_order_id=order_id,
                razorpay_payment_id=payment_id or f'pay_mock_{user_id}'
            )

            profile.payment_status = 'Paid'
            if plan:
                from datetime import timedelta
                from django.utils import timezone
                profile.active_plan = plan
                profile.plan_expiry_date = timezone.now() + timedelta(days=plan.duration_months * 30)
            profile.save()
            return JsonResponse({'status': 'success', 'message': 'Payment successful!'})
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({'status': 'error', 'message': 'Invalid payment signature!'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

from django.contrib.auth.decorators import login_required

@login_required
def payment_history(request):
    from .models import Transaction
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'web/payment_history.html', {'transactions': transactions})

@login_required(login_url='/accounts/login/')
def billing(request):
    try:
        user_profile = request.user.profile
        active_plan = user_profile.active_plan
        plan_expiry_date = user_profile.plan_expiry_date
    except Exception:
        active_plan = None
        plan_expiry_date = None

    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')

    context = {
        'active_plan': active_plan,
        'plan_expiry_date': plan_expiry_date,
        'transactions': transactions,
    }
    return render(request, 'payments/billing.html', context)


