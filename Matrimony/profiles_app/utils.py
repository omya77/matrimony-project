from django.utils import timezone

def check_and_update_plan_status(profile):
    if not profile:
        return
    if profile.payment_status == 'Paid' and profile.plan_expiry_date:
        if timezone.now() > profile.plan_expiry_date:
            profile.payment_status = 'Pending'
            profile.active_plan = None
            profile.plan_expiry_date = None
            profile.save()
