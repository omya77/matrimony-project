import os
import re

with open('admin_panel/views.py', 'r', encoding='utf-8') as f:
    views_code = f.read()

# 1. Add toggle_user_status API
toggle_api = """@csrf_exempt
@login_required(login_url='/admin/login/')
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
"""
if 'def toggle_user_status' not in views_code:
    views_code += '\n' + toggle_api

# 2. Add revenue_reports view
revenue_view = """@login_required(login_url='/admin/login/')
def revenue_reports(request):
    # Dummy data for now until Mukta builds Payments
    context = {
        'total_revenue': 45000,
        'this_month': 12000,
        'active_subscriptions': 35
    }
    return render(request, 'admin_panel/revenue_reports.html', context)
"""
if 'def revenue_reports' not in views_code:
    views_code += '\n' + revenue_view

# 3. Add success_stories view
success_view = """from .models import SuccessStory, PlatformSetting
@login_required(login_url='/admin/login/')
def success_stories(request):
    stories = SuccessStory.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/success_stories.html', {'stories': stories})

@csrf_exempt
@login_required(login_url='/admin/login/')
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
"""
if 'def success_stories' not in views_code:
    views_code += '\n' + success_view

# 4. Update auth_security -> platform_settings (rename logically, but keep view name as auth_security for backward compat or just replace)
# Wait, auth_security view is currently:
# def auth_security(request): ...
# I will replace it.
new_settings_view = """def auth_security(request):
    # Also acting as Platform Settings
    settings = PlatformSetting.objects.all()
    if not settings:
        PlatformSetting.objects.create(key='Maintenance Mode', value='False', description='Disable user logins')
        PlatformSetting.objects.create(key='Auto-Approve Photos', value='True', description='Approve photos automatically')
        settings = PlatformSetting.objects.all()
    
    return render(request, 'admin_panel/platform_settings.html', {'settings': settings})

@csrf_exempt
@login_required(login_url='/admin/login/')
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
"""
views_code = re.sub(r'def auth_security\(request\):[\s\S]*?return render\(request, \'admin_panel/auth_security\.html\', context\)', new_settings_view.strip(), views_code)

with open('admin_panel/views.py', 'w', encoding='utf-8') as f:
    f.write(views_code)
print("Updated admin_panel/views.py")
