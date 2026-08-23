from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import redirect


class CustomAccountAdapter(DefaultAccountAdapter):
    """Custom adapter to handle redirects after login/signup."""
    
    def get_login_redirect_url(self, request):
        """After login, check profile completeness and redirect accordingly."""
        user = request.user
        try:
            profile = user.profile
            # If profile has no personal info filled, go to personal info page
            if not profile.full_name or not profile.gender or not profile.dob:
                return '/profiles/personal/'
            # If paid, go directly to search
            if profile.payment_status == 'Paid':
                return '/profiles/search/basic/'
            # If profile is pending approval, go to checkout (under review page)
            if profile.approval_status == 'Pending':
                return '/payments/checkout/'
            # If approved but not paid, go to checkout
            if profile.approval_status == 'Approved' and profile.payment_status != 'Paid':
                return '/payments/checkout/'
            # Fully approved and paid - go to search
            return '/profiles/search/basic/'
        except Exception:
            return '/profiles/personal/'
