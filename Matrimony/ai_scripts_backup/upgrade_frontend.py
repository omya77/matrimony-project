import re

# Premium CSS string
premium_css = """
    <style>
      :root {
        --rose: #e94057;
        --rose-red: #e94057;
        --pink: #ff7aa2;
        --soft-pink: #fff0f2;
        --glass-bg: rgba(255, 255, 255, 0.75);
        --glass-border: rgba(255, 255, 255, 0.4);
      }
      .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(233, 64, 87, 0.08);
        transition: all 0.3s ease;
      }
      .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(233, 64, 87, 0.15);
      }
      .btn-premium-gradient {
        background: linear-gradient(135deg, var(--rose) 0%, var(--pink) 100%);
        color: #fff;
        border: none;
        padding: 10px 24px;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(233, 64, 87, 0.2);
      }
      .btn-premium-gradient:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(233, 64, 87, 0.3);
        color: #fff;
      }
      .text-gradient {
        background: linear-gradient(90deg, #1e293b, #ff4d6d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
      }
    </style>
"""

# 1. Update personal.html
print("Updating personal.html")
with open('Template/web/personal.html', 'r', encoding='utf-8') as f:
    personal_html = f.read()

if 'var(--glass-bg)' not in personal_html:
    personal_html = personal_html.replace('</head>', premium_css + '\n</head>')
    # Update form cards
    personal_html = personal_html.replace('class="form-card"', 'class="form-card glass-card p-4"')
    # Update body background to soft gradient
    personal_html = re.sub(
        r'background-color:\s*#f8f9fa;',
        r'background: linear-gradient(135deg, #fff0f2 0%, #ffe4e8 100%);',
        personal_html
    )
    with open('Template/web/personal.html', 'w', encoding='utf-8') as f:
        f.write(personal_html)

# 2. Update settings.html
print("Updating settings.html")
with open('Template/web/settings.html', 'r', encoding='utf-8') as f:
    settings_html = f.read()

if 'var(--glass-bg)' not in settings_html:
    settings_html = settings_html.replace('</head>', premium_css + '\n</head>')
    # Convert settings cards to glass cards
    settings_html = settings_html.replace(
        'class="card border-0 shadow-sm rounded-4',
        'class="card glass-card border-0'
    )
    # Add gradient body
    if '<body class="bg-light">' in settings_html:
        settings_html = settings_html.replace('<body class="bg-light">', '<body style="background: linear-gradient(135deg, #fff0f2 0%, #f1f5f9 100%);">')
    
    with open('Template/web/settings.html', 'w', encoding='utf-8') as f:
        f.write(settings_html)

# 3. Update my_profile_data.html
print("Updating my_profile_data.html")
with open('Template/web/my_profile_data.html', 'r', encoding='utf-8') as f:
    profile_html = f.read()

if 'btn-premium-gradient' not in profile_html:
    profile_html = profile_html.replace('</head>', premium_css + '\n</head>')
    profile_html = profile_html.replace('class="btn edit-btn w-100"', 'class="btn-premium-gradient w-100"')
    with open('Template/web/my_profile_data.html', 'w', encoding='utf-8') as f:
        f.write(profile_html)

print("User pages updated successfully!")
