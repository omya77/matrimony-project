import os

# Premium Admin CSS
admin_css = """
    <style>
      :root {
        --glass-bg: rgba(255, 255, 255, 0.85);
        --glass-border: rgba(255, 255, 255, 0.5);
      }
      .glass-card {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border) !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.05) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
      }
      .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.1) !important;
      }
      .custom-table {
        background: transparent !important;
      }
      .custom-table thead tr {
        background: rgba(248, 250, 252, 0.8) !important;
      }
      .table-row-hover:hover {
        background: rgba(255, 255, 255, 0.6) !important;
        transform: scale(1.01);
        transition: all 0.2s ease;
      }
    </style>
"""

# Update base_admin.html
with open('Template/admin_panel/base_admin.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

if 'var(--glass-bg)' not in base_html:
    base_html = base_html.replace('</head>', admin_css + '\n</head>')
    with open('Template/admin_panel/base_admin.html', 'w', encoding='utf-8') as f:
        f.write(base_html)

# Update the 3 admin templates to use glass-card
files = [
    'gauri_manage_profiles.html',
    'gauri_photo_approvals.html',
    'gauri_partner_preferences.html'
]

for file in files:
    filepath = os.path.join('Template/admin_panel', file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'class="card-panel glass-card p-4"' not in content:
        content = content.replace('class="card-panel"', 'class="card-panel glass-card p-4"')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("Admin pages updated successfully!")
