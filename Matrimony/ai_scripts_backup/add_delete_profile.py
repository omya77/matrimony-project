import re

# 1. Update accounts_app/views.py
with open('accounts_app/views.py', 'r', encoding='utf-8') as f:
    views_content = f.read()

delete_view = """
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
@csrf_exempt
def delete_account(request):
    if request.method == 'POST':
        try:
            safe_delete_user(request.user)
            return JsonResponse({'status': 'success', 'message': 'Account deleted successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
"""

if 'def delete_account' not in views_content:
    with open('accounts_app/views.py', 'a', encoding='utf-8') as f:
        f.write("\n" + delete_view)
    print("Added delete_account to views.py")

# 2. Update accounts_app/urls.py
with open('accounts_app/urls.py', 'r', encoding='utf-8') as f:
    urls_content = f.read()

if 'delete-account/' not in urls_content:
    urls_content = urls_content.replace(
        "path('settings/', views.settings, name='settings'),",
        "path('settings/', views.settings, name='settings'),\n    path('delete-account/', views.delete_account, name='delete_account'),"
    )
    with open('accounts_app/urls.py', 'w', encoding='utf-8') as f:
        f.write(urls_content)
    print("Added delete-account to urls.py")

# 3. Update Template/web/settings.html
with open('Template/web/settings.html', 'r', encoding='utf-8') as f:
    settings_html = f.read()

delete_card = """
                <div class="card border-0 shadow-sm rounded-4 mt-4 mb-4" style="background: rgba(255, 255, 255, 0.9);">
                    <div class="card-body p-4">
                        <h5 class="card-title fw-bold text-danger mb-3"><i class="fa-solid fa-trash me-2"></i> Delete Account</h5>
                        <hr class="opacity-10 mb-4">
                        <p class="text-muted small mb-4">Once you delete your account, there is no going back. Please be certain.</p>
                        <button id="deleteAccountBtn" class="btn btn-outline-danger rounded-pill px-4 py-2 fw-bold">Delete My Account</button>
                    </div>
                </div>
"""

# Insert delete card before the closing div of the main column (</div></div></div>)
if 'Delete My Account' not in settings_html:
    settings_html = settings_html.replace(
        '            </div>\n        </div>\n    </div>',
        delete_card + '\n            </div>\n        </div>\n    </div>'
    )

    # Add JS for delete button
    js_addition = """
        const deleteBtn = document.getElementById('deleteAccountBtn');
        if (deleteBtn) {
            deleteBtn.addEventListener('click', function() {
                if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
                    fetch('/accounts/delete-account/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': '{{ csrf_token }}'
                        }
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.status === 'success') {
                            alert('Your account has been deleted.');
                            window.location.href = '/';
                        } else {
                            alert('Error: ' + data.message);
                        }
                    })
                    .catch(err => console.error(err));
                }
            });
        }
    """
    settings_html = settings_html.replace('});\n    </script>', js_addition + '\n    });\n    </script>')

    with open('Template/web/settings.html', 'w', encoding='utf-8') as f:
        f.write(settings_html)
    print("Added delete card to settings.html")

