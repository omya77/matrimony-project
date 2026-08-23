import os
import re

# 1. Update URLs
with open('admin_panel/urls.py', 'r', encoding='utf-8') as f:
    urls_html = f.read()

new_urls = """
    # Tejaswini Extensions
    path('api/toggle-user-status/', views.toggle_user_status, name='toggle_user_status'),
    path('revenue-reports/', views.revenue_reports, name='revenue_reports'),
    path('success-stories/', views.success_stories, name='success_stories'),
    path('api/toggle-story-status/', views.toggle_story_status, name='toggle_story_status'),
    path('api/toggle-setting/', views.toggle_setting, name='toggle_setting'),
"""
if 'revenue_reports' not in urls_html:
    urls_html = urls_html.replace(']', new_urls + '\n]')
    with open('admin_panel/urls.py', 'w', encoding='utf-8') as f:
        f.write(urls_html)
    print("Updated admin_panel/urls.py")

# 2. Add Links to base_admin.html
with open('Template/admin_panel/base_admin.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

tejas_links = """
            <!-- 5. Platform Settings (Tejaswini) -->
            <div class="nav-category">Tejaswini - Reports & Settings</div>
            <a href="{% url 'revenue_reports' %}" class="nav-item {% if request.resolver_match.url_name == 'revenue_reports' %}active{% endif %}">
                <i class="fa-solid fa-chart-line"></i> Revenue Reports
            </a>
            <a href="{% url 'success_stories' %}" class="nav-item {% if request.resolver_match.url_name == 'success_stories' %}active{% endif %}">
                <i class="fa-solid fa-heart-circle-check"></i> Success Stories
            </a>
            <a href="{% url 'auth_security' %}" class="nav-item {% if request.resolver_match.url_name == 'auth_security' %}active{% endif %}">
                <i class="fa-solid fa-gear"></i> Platform Settings
            </a>
"""

if 'Tejaswini - Reports & Settings' not in base_html:
    base_html = re.sub(
        r'<!-- 5\. Developer Zone -->',
        tejas_links + '\n            <!-- 5. Developer Zone -->',
        base_html
    )
    with open('Template/admin_panel/base_admin.html', 'w', encoding='utf-8') as f:
        f.write(base_html)

# 3. Update auth_users.html to include Ban button
auth_users_path = 'Template/admin_panel/auth_users.html'
if os.path.exists(auth_users_path):
    with open(auth_users_path, 'r', encoding='utf-8') as f:
        au_html = f.read()
    
    # Add JS
    if 'toggleUserStatus' not in au_html:
        js = """
        <script>
        function toggleUserStatus(userId, btn) {
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
            fetch('/admin_panel/api/toggle-user-status/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId })
            }).then(r => r.json()).then(data => {
                if(data.status === 'success') {
                    location.reload();
                } else {
                    alert(data.message);
                }
            });
        }
        </script>
        """
        au_html = au_html.replace('{% endblock %}', js + '\n{% endblock %}')
        
        # Add button in the loop
        # Finding the Action column
        # Wait, the action column is usually the last <td>. Let's just replace View button or append to it.
        # Let's see what auth_users.html has: <a href="#" class="btn btn-sm btn-outline-primary rounded-pill"><i class="fa-solid fa-eye"></i> View</a>
        action_btn_str = '<a href="#" class="btn btn-sm btn-outline-primary rounded-pill"><i class="fa-solid fa-eye"></i> View</a>'
        new_btns = """
            {% if u.is_superuser %}
                <span class="badge bg-primary">Admin</span>
            {% else %}
                <button onclick="toggleUserStatus({{ u.id }}, this)" class="btn btn-sm rounded-pill {% if u.is_active %}btn-outline-danger{% else %}btn-success{% endif %}">
                    {% if u.is_active %}<i class="fa-solid fa-ban"></i> Ban{% else %}<i class="fa-solid fa-check"></i> Unban{% endif %}
                </button>
            {% endif %}
        """
        au_html = au_html.replace(action_btn_str, action_btn_str + new_btns)
        
        with open(auth_users_path, 'w', encoding='utf-8') as f:
            f.write(au_html)
        print("Updated auth_users.html")

# 4. Create revenue_reports.html
rev_html = """{% extends 'admin_panel/base_admin.html' %}
{% block title %}Revenue Reports - Admin{% endblock %}
{% block content %}
<div class="dashboard-container fade-in-up">
    <div class="page-title-row mb-4">
        <h1 style="background: linear-gradient(90deg, #1e293b, #ff4d6d); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Revenue Reports</h1>
    </div>
    <div class="row mb-4">
        <div class="col-md-4">
            <div class="card-panel glass-card p-4 text-center h-100">
                <i class="fa-solid fa-indian-rupee-sign fa-3x text-success mb-3"></i>
                <h3>₹{{ total_revenue }}</h3>
                <p class="text-muted mb-0">Total Revenue</p>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card-panel glass-card p-4 text-center h-100">
                <i class="fa-solid fa-money-bill-trend-up fa-3x text-primary mb-3"></i>
                <h3>₹{{ this_month }}</h3>
                <p class="text-muted mb-0">This Month</p>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card-panel glass-card p-4 text-center h-100">
                <i class="fa-solid fa-users fa-3x text-warning mb-3"></i>
                <h3>{{ active_subscriptions }}</h3>
                <p class="text-muted mb-0">Active Subscriptions</p>
            </div>
        </div>
    </div>
    
    <div class="card-panel glass-card p-4">
        <h5 class="mb-4">Revenue Chart (Dummy Data)</h5>
        <canvas id="revChart" height="100"></canvas>
    </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    const ctx = document.getElementById('revChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Revenue (₹)',
                data: [12000, 19000, 15000, 22000, 18000, 30000],
                borderColor: '#e94057',
                backgroundColor: 'rgba(233, 64, 87, 0.1)',
                tension: 0.4,
                fill: true
            }]
        }
    });
</script>
{% endblock %}
"""
with open('Template/admin_panel/revenue_reports.html', 'w', encoding='utf-8') as f:
    f.write(rev_html)

# 5. Create success_stories.html
ss_html = """{% extends 'admin_panel/base_admin.html' %}
{% block title %}Manage Success Stories{% endblock %}
{% block content %}
<div class="dashboard-container fade-in-up">
    <div class="page-title-row mb-4">
        <h1 style="background: linear-gradient(90deg, #1e293b, #ff4d6d); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Manage Success Stories</h1>
    </div>
    <div class="card-panel glass-card p-4">
        <div class="table-responsive">
            <table class="table custom-table align-middle">
                <thead>
                    <tr>
                        <th>Couple Name</th>
                        <th>Wedding Date</th>
                        <th>Story</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for s in stories %}
                    <tr>
                        <td class="fw-bold">{{ s.couple_name }}</td>
                        <td>{{ s.wedding_date }}</td>
                        <td>{{ s.story_text|truncatechars:50 }}</td>
                        <td>
                            {% if s.is_approved %}
                            <span class="badge bg-success rounded-pill">Approved</span>
                            {% else %}
                            <span class="badge bg-warning text-dark rounded-pill">Pending</span>
                            {% endif %}
                        </td>
                        <td>
                            <button onclick="toggleStory({{ s.id }}, this)" class="btn btn-sm {% if s.is_approved %}btn-outline-danger{% else %}btn-success{% endif %} rounded-pill">
                                {% if s.is_approved %}Revoke{% else %}Approve{% endif %}
                            </button>
                        </td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="5" class="text-center py-4 text-muted">No success stories yet.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
<script>
function toggleStory(id, btn) {
    btn.innerHTML = '...';
    fetch('/admin_panel/api/toggle-story-status/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ story_id: id })
    }).then(r => r.json()).then(data => location.reload());
}
</script>
{% endblock %}
"""
with open('Template/admin_panel/success_stories.html', 'w', encoding='utf-8') as f:
    f.write(ss_html)

# 6. Create platform_settings.html
ps_html = """{% extends 'admin_panel/base_admin.html' %}
{% block title %}Platform Settings{% endblock %}
{% block content %}
<div class="dashboard-container fade-in-up">
    <div class="page-title-row mb-4">
        <h1 style="background: linear-gradient(90deg, #1e293b, #ff4d6d); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Platform Settings</h1>
        <p class="text-muted">Global configuration switches.</p>
    </div>
    <div class="row g-4">
        {% for s in settings %}
        <div class="col-md-6">
            <div class="card-panel glass-card p-4 d-flex justify-content-between align-items-center">
                <div>
                    <h5 class="fw-bold mb-1">{{ s.key }}</h5>
                    <p class="text-muted small mb-0">{{ s.description }}</p>
                </div>
                <div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" role="switch" style="width: 50px; height: 25px;" {% if s.value == 'True' %}checked{% endif %} onchange="toggleSetting({{ s.id }})">
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
<script>
function toggleSetting(id) {
    fetch('/admin_panel/api/toggle-setting/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ setting_id: id })
    }).then(r => r.json());
}
</script>
{% endblock %}
"""
with open('Template/admin_panel/platform_settings.html', 'w', encoding='utf-8') as f:
    f.write(ps_html)

print("Created all Tejaswini templates.")
