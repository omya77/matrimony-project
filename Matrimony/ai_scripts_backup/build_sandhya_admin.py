import os
import re

# 1. Update base_admin.html
with open('Template/admin_panel/base_admin.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

sandhya_links = """
            <!-- 3. Interactions (Sandhya) -->
            <div class="nav-category">Sandhya - Interactions</div>
            <a href="{% url 'sandhya_match_search' %}" class="nav-item {% if request.resolver_match.url_name == 'sandhya_match_search' %}active{% endif %}">
                <i class="fa-solid fa-magnifying-glass"></i> Match Search Analytics
            </a>
            <a href="{% url 'sandhya_pending_requests' %}" class="nav-item {% if request.resolver_match.url_name == 'sandhya_pending_requests' %}active{% endif %}">
                <i class="fa-solid fa-envelope"></i> Platform Interests
            </a>
"""
# Replace the existing Sandhya block
base_html = re.sub(
    r'<!-- 3\. Interactions \(Sandhya\) -->[\s\S]*?(?=<!-- 4\. Payments \(Mukta\))',
    sandhya_links + '\n            ',
    base_html
)

with open('Template/admin_panel/base_admin.html', 'w', encoding='utf-8') as f:
    f.write(base_html)

# 2. Update admin_panel/urls.py
with open('admin_panel/urls.py', 'r', encoding='utf-8') as f:
    urls_html = f.read()

new_urls = """
    # Sandhya Interactions Admin
    path('interactions/search/', views.sandhya_match_search, name='sandhya_match_search'),
    path('interactions/requests/', views.sandhya_pending_requests, name='sandhya_pending_requests'),
"""
if 'sandhya_match_search' not in urls_html:
    urls_html = urls_html.replace(']', new_urls + '\n]')
    with open('admin_panel/urls.py', 'w', encoding='utf-8') as f:
        f.write(urls_html)

# 3. Update admin_panel/views.py
with open('admin_panel/views.py', 'r', encoding='utf-8') as f:
    views_html = f.read()

new_views = """
from interactions_app.models import InterestRequest

@login_required(login_url='/admin/login/')
def sandhya_match_search(request):
    # Admin view to search across all profiles
    profiles = Profile.objects.all().order_by('-created_at')
    
    query = request.GET.get('q')
    if query:
        profiles = profiles.filter(
            Q(user__username__icontains=query) |
            Q(full_name__icontains=query) |
            Q(city__icontains=query)
        )
        
    return render(request, 'admin_panel/sandhya_match_search.html', {'profiles': profiles, 'query': query})

@login_required(login_url='/admin/login/')
def sandhya_pending_requests(request):
    # View all interest requests happening on the platform
    interests = InterestRequest.objects.all().select_related('sender__profile', 'receiver__profile').order_by('-created_at')
    
    return render(request, 'admin_panel/sandhya_pending_requests.html', {'interests': interests})
"""
if 'def sandhya_match_search' not in views_html:
    with open('admin_panel/views.py', 'a', encoding='utf-8') as f:
        f.write("\n" + new_views)

# 4. Create Templates
t1 = """{% extends 'admin_panel/base_admin.html' %}
{% block title %}Match Search Analytics - Admin{% endblock %}
{% block content %}
<div class="dashboard-container fade-in-up">
    <div class="page-title-row d-flex justify-content-between align-items-center mb-4">
        <h1 style="background: linear-gradient(90deg, #1e293b, #ff4d6d); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Global Match Search</h1>
        <form class="d-flex" method="GET">
            <input type="text" name="q" value="{{ query|default:'' }}" class="form-control rounded-pill me-2" placeholder="Search by name, username, city...">
            <button type="submit" class="btn btn-premium-gradient rounded-pill">Search</button>
        </form>
    </div>
    <div class="card-panel glass-card p-4">
        <div class="table-responsive">
            <table class="table custom-table align-middle">
                <thead>
                    <tr>
                        <th>Profile</th>
                        <th>Name</th>
                        <th>Location</th>
                        <th>Gender / Religion</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for p in profiles %}
                    <tr class="table-row-hover">
                        <td>
                            <img src="{% if p.photo %}{{ p.photo.url }}{% else %}https://ui-avatars.com/api/?name={{ p.full_name|urlencode }}&background=e94057&color=fff{% endif %}" class="rounded-circle shadow-sm" width="45" height="45" style="object-fit: cover;">
                        </td>
                        <td class="fw-bold">{{ p.full_name }}<br><small class="text-muted">{{ p.user.username }}</small></td>
                        <td>{{ p.city }}, {{ p.state }}</td>
                        <td>{{ p.gender }} / {{ p.religion }}</td>
                        <td>
                            <a href="#" class="btn btn-sm btn-outline-primary rounded-pill"><i class="fa-solid fa-eye"></i> View</a>
                        </td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="5" class="text-center py-4 text-muted">No profiles found.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
"""

t2 = """{% extends 'admin_panel/base_admin.html' %}
{% block title %}Platform Interests - Admin{% endblock %}
{% block content %}
<div class="dashboard-container fade-in-up">
    <div class="page-title-row mb-4">
        <h1 style="background: linear-gradient(90deg, #1e293b, #ff4d6d); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Platform Interest Requests</h1>
        <p class="text-muted">Live overview of all connections being made on ForeverBond.</p>
    </div>
    <div class="card-panel glass-card p-4">
        <div class="table-responsive">
            <table class="table custom-table align-middle">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Sender</th>
                        <th>Receiver</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for i in interests %}
                    <tr class="table-row-hover">
                        <td>{{ i.created_at|date:"M d, Y h:i A" }}</td>
                        <td class="fw-bold text-primary">{{ i.sender.profile.full_name|default:i.sender.username }}</td>
                        <td class="fw-bold text-success">{{ i.receiver.profile.full_name|default:i.receiver.username }}</td>
                        <td>
                            {% if i.status == 'pending' %}
                            <span class="badge bg-warning text-dark rounded-pill">Pending</span>
                            {% elif i.status == 'accepted' %}
                            <span class="badge bg-success rounded-pill">Accepted</span>
                            {% else %}
                            <span class="badge bg-danger rounded-pill">Rejected</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="4" class="text-center py-4 text-muted">No interest requests found.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
"""

with open('Template/admin_panel/sandhya_match_search.html', 'w', encoding='utf-8') as f:
    f.write(t1)
with open('Template/admin_panel/sandhya_pending_requests.html', 'w', encoding='utf-8') as f:
    f.write(t2)

print("Sandhya Admin pages created and wired up!")
