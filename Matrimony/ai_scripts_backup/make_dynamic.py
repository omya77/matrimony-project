import os
import re

LOOP_TEMPLATE = """<div class="row g-4">
            {% for match in matches %}
            <div class="col-xl-4 col-sm-6 profile-card-col page-1">
              <div class="profile-card">
                <div class="card-header-img">
                  <div class="badge-top-left"><i class="fa-solid fa-star"></i> Verified</div>
                  <div class="badge-top-right"><i class="fa-solid fa-circle online"></i> Online</div>
                  <div class="badge-bottom-left"><i class="fa-solid fa-heart-pulse"></i> 95% Match</div>
                  <img src="{% if match.photo %}{{ match.photo.url }}{% else %}https://ui-avatars.com/api/?name={{ match.full_name|default:'User'|urlencode }}&background=e94057&color=fff{% endif %}" alt="{{ match.full_name|default:'User' }}" class="verified-glow-img" />
                </div>
                <div class="card-body">
                  <div class="profile-id"><span>ID: SM{{ match.id }}00</span> <span class="recently-active">Active now</span></div>
                  <h3 class="profile-name">{{ match.full_name|default:'ForeverBond User' }} <i class="fa-solid fa-circle-check verified-icon verification-trigger" title="Click to view verification details" style="cursor: pointer;"></i></h3>
                  <p class="short-bio">{{ match.about_me|default:'Looking for a companion with a modern outlook and traditional values.'|truncatewords:15 }}</p>

                  <div class="profile-details-grid">
                    <div class="detail-item"><i class="fa-solid fa-calendar"></i> {{ match.age|default:'N/A' }} Yrs</div>
                    <div class="detail-item"><i class="fa-solid fa-ruler-vertical"></i> {{ match.height|default:'N/A' }}</div>
                    <div class="detail-item"><i class="fa-solid fa-om"></i> {{ match.religion|default:'Hindu' }}</div>
                    <div class="detail-item"><i class="fa-solid fa-users"></i> {{ match.caste|default:'Any' }}</div>
                    <div class="detail-item"><i class="fa-solid fa-graduation-cap"></i> {{ match.highest_education|default:'N/A' }}</div>
                    <div class="detail-item"><i class="fa-solid fa-briefcase"></i> {{ match.profession|default:'N/A' }}</div>
                    <div class="detail-item" style="grid-column: 1 / span 2;"><i class="fa-solid fa-location-dot"></i> {{ match.city|default:'N/A' }}{% if match.state %}, {{ match.state }}{% endif %}</div>
                  </div>

                  <div class="card-actions">
                    <a href="#" class="btn-primary-custom send-interest-action"><i class="fa-solid fa-heart"></i> Send Interest</a>
                    <div class="action-row-2">
                      <a href="#" class="btn-secondary-custom view-profile-btn"><i class="fa-solid fa-eye"></i> View Profile</a>
                      <a href="#" class="btn-secondary-custom"><i class="fa-solid fa-bookmark"></i> Save</a>
                      <a href="/interactions/chat/" class="btn-premium-chat open-chat-action"><i class="fa-solid fa-comment-dots"></i> Chat</a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            {% empty %}
            <div class="col-12 text-center py-5 bg-white shadow-sm" style="border-radius: 12px;">
                <i class="fa-solid fa-users-slash text-muted mb-3" style="font-size: 3rem;"></i>
                <h4 class="text-secondary fw-bold">No profiles found</h4>
                <p class="text-muted">Check back later for new profiles.</p>
            </div>
            {% endfor %}
          </div>"""

files_to_update = [
    'Template/web/verified_profiles.html',
    'Template/web/saved_profiles.html',
    'Template/web/ai_search.html',
    'Template/web/saved_searches.html',
    'Template/web/matches1.html',
    'Template/web/matches2.html',
    'Template/web/Ai-match.html'
]

for filename in files_to_update:
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.search(r'(<div\s+class=["\'\s]*row\s+g-4["\'\s]*>)(.*?)(<!-- Pagination Navigation -->|<nav\s+aria-label="Page navigation)', content, re.DOTALL | re.IGNORECASE)
        if match:
            new_content = content[:match.start(1)] + LOOP_TEMPLATE + '\n' + content[match.start(3):]
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated {filename}')
        else:
            print(f'Pattern not found in {filename}')
