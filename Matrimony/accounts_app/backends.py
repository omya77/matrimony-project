from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Check if the user passed an email instead of a username
        if username and '@' in username:
            user = User.objects.filter(email__iexact=username).first()
            if user and user.check_password(password):
                return user
        
        # Fallback to default username authentication
        return super().authenticate(request, username=username, password=password, **kwargs)
