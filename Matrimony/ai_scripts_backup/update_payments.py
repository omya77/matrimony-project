import os
import re

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\payments_app\views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Update checkout
new_checkout = '''def checkout(request):
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
            
    context = {
        'razorpay_key_id': RAZORPAY_KEY_ID,
        'plan': plan
    }
    return render(request, 'web/checkout.html', context)'''

# We need to replace the entire checkout function.
content = re.sub(r'def checkout\(request\):.*?return render\(request, \'web/checkout\.html\', context\)', new_checkout, content, flags=re.DOTALL)

# Update verify_payment to log transaction
old_verify = '''            # Verification successful, update profile
            profile = Profile.objects.get(user=request.user)
            profile.payment_status = 'Paid'
            profile.save()
            
            return JsonResponse({'status': 'success', 'message': 'Payment successful!'})'''

new_verify = '''            # Verification successful, update profile
            profile = Profile.objects.get(user=request.user)
            profile.payment_status = 'Paid'
            profile.save()
            
            # Log Transaction
            selected_plan_id = request.session.get('selected_plan_id')
            plan = None
            if selected_plan_id:
                from .models import MembershipPlan
                plan = MembershipPlan.objects.filter(id=selected_plan_id).first()
                
            from .models import Transaction
            Transaction.objects.create(
                user=request.user,
                plan=plan,
                amount=plan.price if plan else 999,
                status='Success',
                razorpay_order_id=order_id,
                razorpay_payment_id=payment_id
            )
            
            return JsonResponse({'status': 'success', 'message': 'Payment successful!'})'''
            
content = content.replace(old_verify, new_verify)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated payments views.')
