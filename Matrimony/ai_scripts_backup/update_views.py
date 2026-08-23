import os

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\admin_panel\views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add admin_login view
login_view_code = '''
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages

def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_superuser or user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'You do not have admin access.')
        else:
            messages.error(request, 'Invalid credentials.')
            
    return render(request, 'admin_panel/admin_login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')
'''

if 'def admin_login(' not in content:
    lines = content.split('\n')
    import_index = 0
    for i, line in enumerate(lines):
        if line.startswith('def '):
            import_index = i
            break
            
    # Insert new views just before the first existing def
    lines.insert(import_index, login_view_code)
    
    # Protect other views
    new_lines = []
    for line in lines:
        if line.startswith('def '):
            func_name = line.split('def ')[1].split('(')[0]
            if func_name not in ['admin_login', 'admin_logout']:
                new_lines.append('@login_required(login_url="/admin_panel/login/")')
        new_lines.append(line)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    print('Added admin login view and protected other views.')
else:
    print('Login view already exists.')
