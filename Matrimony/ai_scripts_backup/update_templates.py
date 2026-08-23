import os
import re

template_dir = r"c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web"

new_actions_block = """          <div class="card-actions-row" style="margin-top: auto;">
            {% if match.interest_status == 'accepted' %}
                <button class="btn-premium-gradient" style="background: linear-gradient(135deg, #10b981 0%, #34d399 100%); pointer-events: none;" disabled><i class="fa-solid fa-user-check"></i> Following</button>
            {% elif match.interest_status == 'pending' %}
                <button class="btn-premium-gradient" style="background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%); pointer-events: none;" disabled><i class="fa-solid fa-clock"></i> Pending</button>
            {% else %}
                <button class="btn-premium-gradient send-interest-action" data-user-id="{{ match.user.id }}" onclick="sendInterest({{ match.user.id }}, this)">Express Interest</button>
            {% endif %}
            <div class="btn-msg-stacked" onclick="openChat({{ match.user.id }})" style="cursor: pointer;" title="Send Message">
              <i class="fa-regular fa-comment-dots"></i>
              <span>Message</span>
            </div>
          </div>"""

for filename in os.listdir(template_dir):
    if not filename.endswith(".html"):
        continue
    
    # We skip advanced_search.html and basic_search.html because they are already perfect/have different structures
    if filename in ["advanced_search.html", "basic_search.html"]:
        continue
        
    filepath = os.path.join(template_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # We look for <div class="card-actions-row"
    # and replace everything from that line up to the closing </div> of card-actions-row
    # We can use regex with DOTALL, matching <div class="card-actions-row".*?<span>Message</span>\s*</div>\s*</div>
    
    pattern = r'<div class="card-actions-row".*?<span>Message</span>\s*</div>\s*</div>'
    
    if re.search(pattern, content, flags=re.DOTALL):
        content = re.sub(pattern, new_actions_block, content, flags=re.DOTALL)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filename}")
