import os

# 1. Update URLs
with open('admin_panel/urls.py', 'r', encoding='utf-8') as f:
    urls_content = f.read()

new_urls = """
    # Gauri Modules
    path('profiles/manage/', views.gauri_manage_profiles, name='gauri_manage_profiles'),
    path('profiles/photos/', views.gauri_photo_approvals, name='gauri_photo_approvals'),
    path('profiles/preferences/', views.gauri_partner_preferences, name='gauri_partner_preferences'),
]"""

if 'gauri_manage_profiles' not in urls_content:
    urls_content = urls_content.replace(']', new_urls)
    with open('admin_panel/urls.py', 'w', encoding='utf-8') as f:
        f.write(urls_content)
    print("Updated urls.py")

# 2. Update Views
new_views = """
from profiles_app.models import Profile

@login_required(login_url='/admin/login/')
def gauri_manage_profiles(request):
    profiles = Profile.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/gauri_manage_profiles.html', {'profiles': profiles})

@login_required(login_url='/admin/login/')
def gauri_photo_approvals(request):
    profiles = Profile.objects.exclude(photo='').exclude(photo__isnull=True).order_by('-created_at')
    return render(request, 'admin_panel/gauri_photo_approvals.html', {'profiles': profiles})

@login_required(login_url='/admin/login/')
def gauri_partner_preferences(request):
    profiles = Profile.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/gauri_partner_preferences.html', {'profiles': profiles})
"""
with open('admin_panel/views.py', 'r', encoding='utf-8') as f:
    if 'gauri_manage_profiles' not in f.read():
        with open('admin_panel/views.py', 'a', encoding='utf-8') as f2:
            f2.write("\n" + new_views)
        print("Updated views.py")

# 3. Update base_admin.html sidebar links
with open('Template/admin_panel/base_admin.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

if 'gauri_manage_profiles' not in base_html:
    base_html = base_html.replace(
        '<a href="#" class="nav-item">\n                <i class="fa-solid fa-users"></i> Manage Profiles\n            </a>',
        '<a href="{% url \'gauri_manage_profiles\' %}" class="nav-item {% if request.resolver_match.url_name == \'gauri_manage_profiles\' %}active{% endif %}">\n                <i class="fa-solid fa-users"></i> Manage Profiles\n            </a>'
    )
    base_html = base_html.replace(
        '<a href="#" class="nav-item">\n                <i class="fa-solid fa-image"></i> Photo Approvals\n            </a>',
        '<a href="{% url \'gauri_photo_approvals\' %}" class="nav-item {% if request.resolver_match.url_name == \'gauri_photo_approvals\' %}active{% endif %}">\n                <i class="fa-solid fa-image"></i> Photo Approvals\n            </a>'
    )
    base_html = base_html.replace(
        '<a href="#" class="nav-item">\n                <i class="fa-solid fa-sliders"></i> Partner Preferences\n            </a>',
        '<a href="{% url \'gauri_partner_preferences\' %}" class="nav-item {% if request.resolver_match.url_name == \'gauri_partner_preferences\' %}active{% endif %}">\n                <i class="fa-solid fa-sliders"></i> Partner Preferences\n            </a>'
    )
    with open('Template/admin_panel/base_admin.html', 'w', encoding='utf-8') as f:
        f.write(base_html)
    print("Updated base_admin.html")

# 4. Create Templates
def create_template(filename, title, th_list, td_logic, extra_logic=""):
    template = f"""{{% extends 'admin_panel/base_admin.html' %}}

{{% block title %}}{title} - Admin Panel{{% endblock %}}

{{% block content %}}
<div class="dashboard-container fade-in-up">
    <div class="page-title-row">
        <div>
            <h1 style="background: linear-gradient(90deg, #1e293b, #ff4d6d); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title}</h1>
        </div>
    </div>
    {extra_logic}
    <div class="card-panel">
        <div class="table-responsive">
            <table class="custom-table" style="box-shadow: 0 0 0 1px #e2e8f0; border-radius: 8px; overflow: hidden;">
                <thead>
                    <tr style="background: #f8fafc;">
                        {''.join(f'<th>{th}</th>' for th in th_list)}
                    </tr>
                </thead>
                <tbody>
                    {{% for profile in profiles %}}
                    <tr class="table-row-hover">
                        {td_logic}
                    </tr>
                    {{% empty %}}
                    <tr>
                        <td colspan="{len(th_list)}" class="text-center text-muted" style="padding: 40px;">
                            <div style="font-size: 3rem; color: #e2e8f0; margin-bottom: 15px;"><i class="fa-solid fa-folder-open"></i></div>
                            <div style="font-weight: 500;">No profiles found.</div>
                        </td>
                    </tr>
                    {{% endfor %}}
                </tbody>
            </table>
        </div>
    </div>
</div>
{{% endblock %}}
"""
    with open(os.path.join('Template/admin_panel', filename), 'w', encoding='utf-8') as f:
        f.write(template)

# Manage Profiles
create_template(
    'gauri_manage_profiles.html',
    'Manage Profiles',
    ['User', 'Matrimony ID', 'Mobile', 'City', 'Status', 'Actions'],
    """
                        <td>
                            <div class="user-cell">
                                <div class="user-avatar" style="box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                                    {% if profile.photo %}
                                        <img src="{{ profile.photo.url }}" alt="">
                                    {% else %}
                                        <div class="avatar-placeholder"><i class="fa-solid fa-user"></i></div>
                                    {% endif %}
                                </div>
                                <div class="user-details">
                                    <span class="name" style="font-size: 0.95rem;">{{ profile.full_name|default:profile.user.username }}</span>
                                    <span class="id" style="color: #64748b; font-size: 0.75rem;">{{ profile.user.email }}</span>
                                </div>
                            </div>
                        </td>
                        <td style="font-weight: 600;">{{ profile.matrimony_id|default:"N/A" }}</td>
                        <td>{{ profile.mobile|default:"N/A" }}</td>
                        <td>{{ profile.city|default:"N/A" }}</td>
                        <td>
                            <span class="status-badge {% if profile.approval_status == 'Approved' %}verified{% elif profile.approval_status == 'Rejected' %}inactive{% else %}pending{% endif %}">
                                {{ profile.approval_status }}
                            </span>
                        </td>
                        <td>
                            <button onclick="deleteUser('{{ profile.id }}')" class="btn btn-sm btn-outline-danger"><i class="fa-solid fa-trash me-1"></i>Delete</button>
                        </td>
    """,
    """
    <script>
    function deleteUser(profileId) {
        if(confirm('Are you sure you want to PERMANENTLY DELETE this user from the database?')) {
            fetch('/admin_panel/api/delete_user/', {
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
)

# Photo Approvals
create_template(
    'gauri_photo_approvals.html',
    'Photo Approvals Queue',
    ['Photo', 'User Details', 'Upload Date', 'Status', 'Actions'],
    """
                        <td>
                            <img src="{{ profile.photo.url }}" alt="" style="width: 80px; height: 80px; border-radius: 8px; object-fit: cover; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                        </td>
                        <td>
                            <div style="font-weight: 600;">{{ profile.full_name|default:profile.user.username }}</div>
                            <div style="font-size: 0.8rem; color: #64748b;">{{ profile.matrimony_id|default:"Pending ID" }}</div>
                        </td>
                        <td>{{ profile.updated_at|date:"d M Y, h:i A" }}</td>
                        <td><span class="status-badge verified">Uploaded</span></td>
                        <td>
                            <button class="btn btn-sm btn-outline-success"><i class="fa-solid fa-check me-1"></i>Approve</button>
                            <button class="btn btn-sm btn-outline-danger"><i class="fa-solid fa-xmark me-1"></i>Reject</button>
                        </td>
    """
)

# Partner Preferences
create_template(
    'gauri_partner_preferences.html',
    'Partner Preferences',
    ['User', 'Age Preference', 'Religion Preference', 'Marital Status'],
    """
                        <td>
                            <div style="font-weight: 600;">{{ profile.full_name|default:profile.user.username }}</div>
                            <div style="font-size: 0.8rem; color: #64748b;">{{ profile.matrimony_id|default:"N/A" }}</div>
                        </td>
                        <td>
                            {% if profile.pref_age_min and profile.pref_age_max %}
                                <span class="badge bg-light text-dark border">{{ profile.pref_age_min }} - {{ profile.pref_age_max }} yrs</span>
                            {% else %}
                                <span class="text-muted">Not specified</span>
                            {% endif %}
                        </td>
                        <td>{{ profile.pref_religion|default:"<span class='text-muted'>Any</span>"|safe }}</td>
                        <td><span class="badge bg-light text-dark border">Not specified</span></td>
    """
)

print("Created 3 HTML templates")
