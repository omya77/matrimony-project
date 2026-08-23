from django.shortcuts import render
from django.urls import resolve
from admin_panel.models import PlatformSetting

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow requests to the admin panel so admins can turn off maintenance mode
        if request.path.startswith('/admin_panel/'):
            return self.get_response(request)
            
        # Check if maintenance mode is enabled
        try:
            maintenance_setting = PlatformSetting.objects.get(key='Maintenance Mode')
            is_maintenance = maintenance_setting.value == 'True'
        except PlatformSetting.DoesNotExist:
            is_maintenance = False

        if is_maintenance:
            # If it's a superuser, you might want to let them bypass it
            if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
                return self.get_response(request)
                
            return render(request, 'maintenance.html', status=503)

        return self.get_response(request)
