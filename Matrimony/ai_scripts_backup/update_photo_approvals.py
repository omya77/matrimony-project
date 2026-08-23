import re

# 1. Update profiles_app/views.py
with open('profiles_app/views.py', 'r', encoding='utf-8') as f:
    profiles_views = f.read()

# Add is_photo_approved = False when photo is uploaded
profiles_views = profiles_views.replace(
    'profile.photo = request.FILES[\'photo\']',
    'profile.photo = request.FILES[\'photo\']\n                profile.is_photo_approved = False'
)
with open('profiles_app/views.py', 'w', encoding='utf-8') as f:
    f.write(profiles_views)

# 2. Update admin_panel/views.py
with open('admin_panel/views.py', 'r', encoding='utf-8') as f:
    admin_views = f.read()

new_admin_views = """
@login_required(login_url='/admin/login/')
@csrf_exempt
def approve_photo(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        profile_id = data.get('profile_id')
        try:
            profile = Profile.objects.get(id=profile_id)
            profile.is_photo_approved = True
            profile.save()
            return JsonResponse({'status': 'success'})
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Profile not found'}, status=404)
    return JsonResponse({'status': 'error'}, status=405)

@login_required(login_url='/admin/login/')
@csrf_exempt
def reject_photo(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        profile_id = data.get('profile_id')
        try:
            profile = Profile.objects.get(id=profile_id)
            profile.photo = None
            profile.is_photo_approved = False
            profile.save()
            return JsonResponse({'status': 'success'})
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Profile not found'}, status=404)
    return JsonResponse({'status': 'error'}, status=405)
"""

if 'def approve_photo' not in admin_views:
    # Update gauri_photo_approvals view to filter out approved photos
    admin_views = admin_views.replace(
        "Profile.objects.exclude(photo='').exclude(photo__isnull=True).order_by('-created_at')",
        "Profile.objects.exclude(photo='').exclude(photo__isnull=True).filter(is_photo_approved=False).order_by('-created_at')"
    )
    with open('admin_panel/views.py', 'a', encoding='utf-8') as f:
        f.write("\n" + new_admin_views)

# 3. Update admin_panel/urls.py
with open('admin_panel/urls.py', 'r', encoding='utf-8') as f:
    urls_content = f.read()

if 'api/approve_photo/' not in urls_content:
    urls_content = urls_content.replace(
        "path('api/delete_user/', views.delete_user, name='delete_user'),",
        "path('api/delete_user/', views.delete_user, name='delete_user'),\n    path('api/approve_photo/', views.approve_photo, name='approve_photo'),\n    path('api/reject_photo/', views.reject_photo, name='reject_photo'),"
    )
    with open('admin_panel/urls.py', 'w', encoding='utf-8') as f:
        f.write(urls_content)

# 4. Update gauri_photo_approvals.html
with open('Template/admin_panel/gauri_photo_approvals.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

if 'approvePhoto' not in html_content:
    html_content = html_content.replace(
        '<button class="btn btn-sm btn-outline-success"><i class="fa-solid fa-check me-1"></i>Approve</button>',
        '<button onclick="approvePhoto({{ profile.id }})" class="btn btn-sm btn-outline-success"><i class="fa-solid fa-check me-1"></i>Approve</button>'
    ).replace(
        '<button class="btn btn-sm btn-outline-danger"><i class="fa-solid fa-xmark me-1"></i>Reject</button>',
        '<button onclick="rejectPhoto({{ profile.id }})" class="btn btn-sm btn-outline-danger"><i class="fa-solid fa-xmark me-1"></i>Reject</button>'
    )
    
    js_addition = """
    <script>
    function approvePhoto(profileId) {
        if(confirm('Approve this photo?')) {
            fetch('/admin_panel/api/approve_photo/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': '{{ csrf_token }}' },
                body: JSON.stringify({ profile_id: profileId })
            }).then(res => res.json()).then(data => {
                if(data.status === 'success') { location.reload(); }
                else { alert('Error: ' + data.message); }
            });
        }
    }
    function rejectPhoto(profileId) {
        if(confirm('Reject this photo? The user will have to upload a new one.')) {
            fetch('/admin_panel/api/reject_photo/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': '{{ csrf_token }}' },
                body: JSON.stringify({ profile_id: profileId })
            }).then(res => res.json()).then(data => {
                if(data.status === 'success') { location.reload(); }
                else { alert('Error: ' + data.message); }
            });
        }
    }
    </script>
    """
    html_content = html_content.replace('{% endblock %}', js_addition + '\n{% endblock %}')
    
    with open('Template/admin_panel/gauri_photo_approvals.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

print("Updated photo approval functionality successfully!")
