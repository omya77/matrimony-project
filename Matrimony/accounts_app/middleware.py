from django.utils import timezone

class PremiumExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                if profile.payment_status == 'Paid' and profile.plan_expiry_date:
                    if timezone.now() > profile.plan_expiry_date:
                        profile.payment_status = 'Pending'
                        profile.plan_expiry_date = None
                        profile.save()
            except Exception:
                pass

        response = self.get_response(request)
        return response
