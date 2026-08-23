import re

# 1. Update context processors
filepath_cp = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\interactions_app\context_processors.py'
with open(filepath_cp, 'r', encoding='utf-8') as f:
    cp = f.read()

old_cp_req = "unread_requests_count = InterestRequest.objects.filter(receiver=request.user, status='pending').count()"
new_cp_req = "unread_requests_count = InterestRequest.objects.filter(receiver=request.user, status='pending', is_viewed=False).count()"
cp = cp.replace(old_cp_req, new_cp_req)

with open(filepath_cp, 'w', encoding='utf-8') as f:
    f.write(cp)

# 2. Update views.py requests function
filepath_views = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\interactions_app\views.py'
with open(filepath_views, 'r', encoding='utf-8') as f:
    views = f.read()

old_req = '''@login_required(login_url='/accounts/login/')
def requests(request):
    # Fetch received requests that are pending
    pending_received = InterestRequest.objects.filter(receiver=request.user, status='pending').select_related('sender__profile')'''

new_req = '''@login_required(login_url='/accounts/login/')
def requests(request):
    # Fetch received requests that are pending
    pending_received = InterestRequest.objects.filter(receiver=request.user, status='pending').select_related('sender__profile')
    
    # Mark as viewed since the user opened the requests page
    InterestRequest.objects.filter(receiver=request.user, status='pending', is_viewed=False).update(is_viewed=True)'''

views = views.replace(old_req, new_req)

with open(filepath_views, 'w', encoding='utf-8') as f:
    f.write(views)

print("Updated python files for viewed logic")
