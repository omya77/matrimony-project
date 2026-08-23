import os
import re

filepath = r"c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web\advanced_search.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add matches2.css to head
if 'matches2.css' not in content:
    content = content.replace(
        '<link rel="stylesheet" href="/static/web/css/glass-card.css" />',
        '<link rel="stylesheet" href="/static/web/css/glass-card.css" />\n    <link rel="stylesheet" href="/static/web/css/matches2.css" />'
    )
    if 'matches2.css' not in content:
        # Fallback if glass-card.css is not there
        content = content.replace(
            '</style>',
            '</style>\n    <link rel="stylesheet" href="/static/web/css/matches2.css" />'
        )

# 2. Replace the cards loop
new_loop = """<div class="pm-profile-container">
        {% for match in matches %}
        <div class="pm-profile-card">
            <div class="pm-profile-image-box">
                <img src="{% if match.photo %}{{ match.photo.url }}{% else %}https://ui-avatars.com/api/?name={{ match.full_name|default:'User'|urlencode }}&background=e94057&color=fff{% endif %}">
            </div>

            <div class="pm-profile-details">
                <div class="pm-profile-header">
                    {% if match.approval_status == 'Approved' %}
                    <span class="pm-verified-badge">
                        ✓ Verified
                    </span>
                    {% endif %}
                    <button class="pm-bookmark-btn" title="Save Profile">
                        <i class="bi bi-bookmark"></i>
                    </button>
                </div>

                <h3>{{ match.full_name|default:'ForeverBond User' }}</h3>

                <p class="pm-age">
                    {{ match.age|default:'N/A' }} Yrs • {{ match.height|default:"N/A" }}
                </p>

                <div class="pm-user-info">
                    <p class="card-edu">🎓 {{ match.highest_education|default:"N/A" }}</p>
                    <p class="card-prof">💼 {{ match.profession|default:"N/A" }}</p>
                    <p class="card-lang">💬 {{ match.mother_tongue|default:"N/A" }}</p>
                    <p class="card-loc">📍 {{ match.city|default:"N/A" }}{% if match.state %}, {{ match.state }}{% endif %}</p>
                    <p class="card-rel">🕉️ {{ match.religion|default:"N/A" }}</p>
                    <p class="card-caste">👥 {{ match.caste|default:"N/A" }}</p>
                </div>

                <div class="pm-card-buttons">
                    <button type="button" class="pm-biodata-btn" data-bs-toggle="modal" data-bs-target="#profileModal{{ match.user.id }}" style="width: 100%; border-radius: 25px; padding: 12px 0; border: none; background: linear-gradient(135deg, #e94057 0%, #ff5c75 100%); color: white; font-weight: 600; cursor: pointer; transition: all 0.3s ease; display: inline-flex; justify-content: center; align-items: center;">
                        <i class="fa-regular fa-eye" style="margin-right: 6px;"></i> View Profile
                    </button>
                </div>
            </div>

            <div class="pm-match-score">
                <b>95%</b>
                <span>Match</span>
            </div>
        </div>
        {% empty %}
        <div class="text-center w-100 p-5" style="grid-column: 1 / -1; background: #fff; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
            <i class="fa-solid fa-users-slash mb-3" style="font-size: 3rem; color: #cbd5e1;"></i>
            <h4 style="color: #475569; font-weight: 600; margin-bottom: 8px;">No matches found</h4>
            <p style="color: #94a3b8; font-size: 14px;">Try adjusting your advanced search criteria or check back later.</p>
        </div>
        {% endfor %}
      </div>"""

# Replace `<div class="advanced-grid"> ... </div>` loop with `pm-profile-container` loop
# Use regex to find and replace
pattern = re.compile(r'<div class="advanced-grid">\s*\{% for match in matches %\}.*?\{% endfor %\}\s*</div>', re.DOTALL)
content = pattern.sub(new_loop, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated advanced_search.html")
