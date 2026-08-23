from django.utils import timezone
from datetime import timedelta

class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Skip static and media files to avoid hitting DB and exhausting connection pools
        if request.path.startswith('/media/') or request.path.startswith('/static/'):
            return response
            
        # We only update last_activity if user is authenticated and has a profile
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                now = timezone.now()
                # Only update if last_activity is missing or older than 5 minutes
                if not profile.last_activity or (now - profile.last_activity) > timedelta(minutes=5):
                    profile.last_activity = now
                    profile.save(update_fields=['last_activity'])
            except Exception:
                pass
                
        return response
