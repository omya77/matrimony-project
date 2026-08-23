import os
import re

template_dir = r"c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web"

new_glass_actions = """          <div class="card-actions-row" style="margin-top: auto; padding-top: 15px;">
             <button type="button" class="btn-premium-gradient" data-bs-toggle="modal" data-bs-target="#profileModal{{ match.user.id }}" style="width: 100%; border-radius: 25px; padding: 12px 0;">
                <i class="fa-regular fa-eye" style="margin-right: 6px;"></i> View Profile
             </button>
          </div>
          {% include 'web/profile_modal.html' %}"""

new_pm_actions = """        <div class="pm-card-buttons">
            <button type="button" class="pm-biodata-btn" data-bs-toggle="modal" data-bs-target="#profileModal{{ match.user.id }}" style="width: 100%; border-radius: 25px; background: #e2e8f0; color: #475569; font-weight: 600;">
                <i class="fa-regular fa-eye" style="margin-right: 6px;"></i> View Profile
            </button>
        </div>
        {% include 'web/profile_modal.html' %}"""

for filename in os.listdir(template_dir):
    if not filename.endswith(".html"):
        continue
    
    if filename in ["advanced_search.html", "basic_search.html", "profile_modal.html", "featured_brides.html"]:
        continue
        
    filepath = os.path.join(template_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace glass card actions
    pattern_glass = r'<div class="card-actions-row" style="margin-top: auto;">.*?<span>Message</span>\s*</div>\s*</div>'
    if re.search(pattern_glass, content, flags=re.DOTALL):
        content = re.sub(pattern_glass, new_glass_actions, content, flags=re.DOTALL)
        
    # Replace pm card actions
    pattern_pm = r'<div class="pm-card-buttons">.*?<i class="fa-regular fa-comment-dots"></i></button>\s*</div>'
    if re.search(pattern_pm, content, flags=re.DOTALL):
        content = re.sub(pattern_pm, new_pm_actions, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filename}")
