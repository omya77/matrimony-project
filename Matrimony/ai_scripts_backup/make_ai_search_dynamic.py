import re

TEMPLATE = """<div class="profile-container">
        {% for match in matches %}
        <div class="glass-card">
          <div class="image-container-gold">
            <img
              src="{% if match.photo %}{{ match.photo.url }}{% else %}https://ui-avatars.com/api/?name={{ match.full_name|default:'User'|urlencode }}&background=e94057&color=fff{% endif %}"
              alt="{{ match.full_name|default:'User' }}"
            />
          </div>
          <h3 class="profile-name-dark">{{ match.full_name|default:'ForeverBond User' }}</h3>

          <div class="profile-details-dark">
            <p>
              <i class="fa-solid fa-user"></i>
              <span
                ><strong>Age:</strong> {{ match.age|default:'N/A' }} &nbsp;&nbsp;
                <strong>Height:</strong> {{ match.height|default:'N/A' }}</span
              >
            </p>
            <p>
              <i class="fa-solid fa-graduation-cap"></i>
              <span><strong>Education:</strong> {{ match.highest_education|default:'N/A' }}</span>
            </p>
            <p>
              <i class="fa-solid fa-briefcase"></i>
              <span><strong>Occupation:</strong> {{ match.profession|default:'N/A' }}</span>
            </p>
            <p>
              <i class="fa-solid fa-location-dot"></i>
              <span><strong>Location:</strong> {{ match.city|default:'N/A' }}{% if match.state %}, {{ match.state }}{% endif %}</span>
            </p>
          </div>

          <div class="card-actions-row">
            <button class="btn-premium-gradient">Express Interest</button>
            <div class="btn-msg-stacked">
              <i class="fa-regular fa-comment-dots"></i>
              <span>Message</span>
            </div>
          </div>
        </div>
        {% empty %}
        <div class="col-12 text-center py-5">
            <h4>No profiles found</h4>
        </div>
        {% endfor %}
      </div>"""

with open('Template/web/ai_search.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'<div class="profile-container">(.*?)</div>\s*</section>', content, re.DOTALL)
if match:
    new_content = content[:match.start()] + TEMPLATE + '\n    </section>' + content[match.end():]
    with open('Template/web/ai_search.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Updated ai_search.html")
else:
    print("Pattern not found in ai_search.html")
