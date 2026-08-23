import os
import re

template_dir = r"c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web"

new_pm_buttons = """        <div class="pm-card-buttons">
            <button class="pm-biodata-btn">View Biodata</button>
            {% if match.interest_status == 'accepted' %}
                <button class="pm-interest-btn" style="background: #10b981; pointer-events: none;" disabled><i class="fa-solid fa-user-check"></i> Following</button>
            {% elif match.interest_status == 'pending' %}
                <button class="pm-interest-btn" style="background: #f59e0b; pointer-events: none;" disabled><i class="fa-solid fa-clock"></i> Pending</button>
            {% else %}
                <button class="pm-interest-btn send-interest-action" data-user-id="{{ match.user.id }}" onclick="sendInterest({{ match.user.id }}, this)">➤ Send Interest</button>
            {% endif %}
            <button class="pm-biodata-btn" onclick="openChat({{ match.user.id }})" style="width: auto; padding: 10px 15px; margin-left: 5px;" title="Send Message"><i class="fa-regular fa-comment-dots"></i></button>
        </div>"""

for filename in os.listdir(template_dir):
    if not filename.endswith(".html"):
        continue
    
    filepath = os.path.join(template_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    pattern = r'<div class="pm-card-buttons">.*?</div>'
    
    if re.search(pattern, content, flags=re.DOTALL):
        # don't replace if it already has 'interest_status' inside
        match_block = re.search(pattern, content, flags=re.DOTALL).group(0)
        if "interest_status" not in match_block:
            content = re.sub(pattern, new_pm_buttons, content, flags=re.DOTALL)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {filename}")
