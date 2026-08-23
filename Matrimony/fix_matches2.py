import re

file_path = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony-2807-2\Matrimony\Matrimony\Template\web\matches2.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the container start
container_idx = content.find('<div class="pm-profile-container">')
if container_idx == -1:
    print("Container not found")
    exit(1)

# Find the end of the container (the section closing tag is a good marker)
end_section_idx = content.find('</section>', container_idx)

prefix = content[:container_idx + len('<div class="pm-profile-container">')]
suffix = content[end_section_idx:]

dynamic_card = """
{% if matches %}
    {% for match in matches %}
    <div class="pm-profile-card">
        <!-- IMAGE SECTION -->
        <div class="pm-profile-image-box">
            <img src="{% if match.photo %}{{ match.photo.url }}{% else %}https://ui-avatars.com/api/?name={{ match.full_name|default:match.user.username|urlencode }}&background=e94057&color=fff{% endif %}" style="object-fit: contain; width: 100%; height: 100%; background: #f8fafc;">
        </div>

        <!-- DETAILS SECTION -->
        <div class="pm-profile-details">
            <div class="pm-profile-header">
                <span class="pm-verified-badge">✓ Verified</span>
                <button class="pm-bookmark-btn">♡</button>
            </div>
            <h3>{{ match.full_name|default:match.user.username }}</h3>
            <p class="pm-age">{{ match.age|default:"N/A" }} Yrs • {{ match.height|default:"N/A" }}</p>

            <div class="pm-user-info">
                <p class="card-edu">🎓 {{ match.highest_education|default:"N/A" }}</p>
                <p class="card-prof">💼 {{ match.profession|default:"N/A" }}</p>
                <p class="card-lang">💬 {{ match.mother_tongue|default:"N/A" }}</p>
                <p class="card-loc">📍 {{ match.city|default:"N/A" }}{% if match.state %}, {{ match.state }}{% endif %}</p>
                <p class="card-rel">🕉️ {{ match.religion|default:"N/A" }}</p>
                <p class="card-caste">👥 {{ match.caste|default:"N/A" }}</p>
            </div>

            <!-- BUTTONS -->
            <div class="pm-card-buttons" style="display: flex; gap: 10px;">
                <button type="button" class="pm-biodata-btn" data-bs-toggle="modal" data-bs-target="#profileModal{{ match.user.id }}" style="flex: 1; border-radius: 25px; padding: 10px 0; border: none; background: linear-gradient(135deg, #e94057 0%, #ff5c75 100%); color: white; font-weight: 600; cursor: pointer;">
                    <i class="fa-regular fa-eye"></i> View Profile
                </button>
                {% if match.interest_status == 'pending' %}
                    <button type="button" class="pm-biodata-btn" style="flex: 1; border-radius: 25px; padding: 10px 0; border: none; background: #6c757d; color: white; font-weight: 600; cursor: not-allowed;" disabled>
                        Pending
                    </button>
                {% elif match.interest_status == 'accepted' %}
                    <button type="button" class="pm-biodata-btn" style="flex: 1; border-radius: 25px; padding: 10px 0; border: none; background: #28a745; color: white; font-weight: 600; cursor: not-allowed;" disabled>
                        Connected
                    </button>
                {% else %}
                    <button type="button" class="pm-biodata-btn" onclick="sendInterest('{{ match.user.id }}', this)" style="flex: 1; border-radius: 25px; padding: 10px 0; border: 1px solid #e94057; background: white; color: #e94057; font-weight: 600; cursor: pointer;">
                        <i class="fa-solid fa-user-plus"></i> Connect
                    </button>
                {% endif %}
            </div>
        </div>

        <!-- MATCH SCORE -->
        <div class="pm-match-score">
            <b>96%</b>
            <span>Match</span>
        </div>
    </div>
    {% endfor %}
{% else %}
    <div style="width: 100%; text-align: center; padding: 50px;">
        <h4>No matches found.</h4>
    </div>
{% endif %}
</div>
"""

new_content = prefix + "\n" + dynamic_card + "\n" + suffix

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully replaced static cards with dynamic loop.")
