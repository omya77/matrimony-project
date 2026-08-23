import os
import re

# 1. Update recomended-matches.html
filepath = 'Template/web/recomended-matches.html'
with open(filepath, 'r', encoding='utf-8') as f:
    rec_content = f.read()

# Add match score display on the match card
score_badge = """
                <div style="position: absolute; top: 15px; left: 15px; background: rgba(255, 255, 255, 0.9); padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 0.9rem; color: var(--rose); box-shadow: 0 4px 10px rgba(0,0,0,0.1); z-index: 10;">
                    <i class="fa-solid fa-star"></i> {{ match.match_score }}% Match
                </div>
"""
if 'fa-star' not in rec_content:
    rec_content = rec_content.replace(
        '<div class="card profile-card glass-card h-100 position-relative">',
        '<div class="card profile-card glass-card h-100 position-relative">' + score_badge
    )
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(rec_content)
    print("Updated recommended-matches.html")


# 2. Update requests.html to have 3 tabs
req_filepath = 'Template/web/requests.html'
with open(req_filepath, 'r', encoding='utf-8') as f:
    req_html = f.read()

if 'nav-tabs' not in req_html:
    tabs_html = """
    <div class="glass-card p-4 mb-4" data-aos="fade-up">
        <h2 class="section-title"><i class="fa-solid fa-users text-danger me-2"></i> Connection Manager</h2>
        
        <!-- Tabs -->
        <ul class="nav nav-tabs nav-fill mb-4 mt-4 border-0" id="requestsTab" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active rounded-pill fw-bold" id="received-tab" data-bs-toggle="tab" data-bs-target="#received" type="button" role="tab" style="color: #495057;">Received Requests <span class="badge bg-danger ms-2">{{ pending_received|length }}</span></button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link rounded-pill fw-bold" id="sent-tab" data-bs-toggle="tab" data-bs-target="#sent" type="button" role="tab" style="color: #495057;">Sent Requests <span class="badge bg-secondary ms-2">{{ pending_sent|length }}</span></button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link rounded-pill fw-bold" id="connections-tab" data-bs-toggle="tab" data-bs-target="#connections" type="button" role="tab" style="color: #495057;">My Connections <span class="badge bg-success ms-2">{{ connections|length }}</span></button>
            </li>
        </ul>
        
        <style>
            .nav-tabs .nav-link.active {
                background: linear-gradient(135deg, var(--rose) 0%, var(--pink) 100%) !important;
                color: white !important;
                border: none;
                box-shadow: 0 4px 15px rgba(233, 64, 87, 0.2);
            }
        </style>
        
        <div class="tab-content" id="requestsTabContent">
            <!-- RECEIVED TAB -->
            <div class="tab-pane fade show active" id="received" role="tabpanel">
                <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
                    {% for req in pending_received %}
                    <div class="col" id="req-card-{{ req.sender.id }}">
                        <div class="card profile-card glass-card h-100">
                            <div class="card-body text-center">
                                <img src="{% if req.sender.profile.photo %}{{ req.sender.profile.photo.url }}{% else %}https://ui-avatars.com/api/?name={{ req.sender.username }}&background=e94057&color=fff{% endif %}" class="rounded-circle mb-3 border border-3 border-danger shadow-sm" alt="Profile" style="width: 100px; height: 100px; object-fit: cover;">
                                
                                <h5 class="card-title fw-bold text-dark">{{ req.sender.profile.full_name|default:req.sender.username }}</h5>
                                <p class="text-muted small mb-3">
                                    <i class="fa-solid fa-location-dot"></i> {{ req.sender.profile.city }}, {{ req.sender.profile.state }}<br>
                                    <i class="fa-solid fa-briefcase"></i> {{ req.sender.profile.profession }}
                                </p>
                                
                                <div class="d-flex justify-content-center gap-2">
                                    <button onclick="acceptInterest({{ req.sender.id }})" class="btn btn-premium-gradient w-50">Accept</button>
                                    <button onclick="rejectInterest({{ req.sender.id }})" class="btn btn-outline-secondary w-50" style="border-radius: 25px;">Reject</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% empty %}
                    <div class="col-12 text-center text-muted py-5">
                        <i class="fa-regular fa-envelope-open fa-3x mb-3 text-secondary"></i>
                        <p>No pending requests.</p>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <!-- SENT TAB -->
            <div class="tab-pane fade" id="sent" role="tabpanel">
                <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
                    {% for req in pending_sent %}
                    <div class="col">
                        <div class="card profile-card glass-card h-100 opacity-75">
                            <div class="card-body text-center">
                                <img src="{% if req.receiver.profile.photo %}{{ req.receiver.profile.photo.url }}{% else %}https://ui-avatars.com/api/?name={{ req.receiver.username }}&background=e94057&color=fff{% endif %}" class="rounded-circle mb-3 shadow-sm" alt="Profile" style="width: 100px; height: 100px; object-fit: cover;">
                                <h5 class="card-title fw-bold text-dark">{{ req.receiver.profile.full_name|default:req.receiver.username }}</h5>
                                <p class="text-warning fw-bold mb-0"><i class="fa-solid fa-clock"></i> Waiting for Reply</p>
                            </div>
                        </div>
                    </div>
                    {% empty %}
                    <div class="col-12 text-center text-muted py-5">
                        <p>You haven't sent any requests.</p>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <!-- CONNECTIONS TAB -->
            <div class="tab-pane fade" id="connections" role="tabpanel">
                <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
                    {% for conn in connections %}
                    <div class="col">
                        <div class="card profile-card glass-card h-100" style="border: 2px solid #198754 !important;">
                            <div class="card-body text-center">
                                <!-- Determine the other person in the connection -->
                                {% if conn.sender == request.user %}
                                    {% with other=conn.receiver %}
                                        <img src="{% if other.profile.photo %}{{ other.profile.photo.url }}{% else %}https://ui-avatars.com/api/?name={{ other.username }}&background=198754&color=fff{% endif %}" class="rounded-circle mb-3 shadow-sm" alt="Profile" style="width: 100px; height: 100px; object-fit: cover;">
                                        <h5 class="card-title fw-bold text-dark">{{ other.profile.full_name|default:other.username }}</h5>
                                        <p class="text-muted small"><i class="fa-solid fa-phone"></i> {{ other.profile.mobile_number|default:"Hidden" }}</p>
                                    {% endwith %}
                                {% else %}
                                    {% with other=conn.sender %}
                                        <img src="{% if other.profile.photo %}{{ other.profile.photo.url }}{% else %}https://ui-avatars.com/api/?name={{ other.username }}&background=198754&color=fff{% endif %}" class="rounded-circle mb-3 shadow-sm" alt="Profile" style="width: 100px; height: 100px; object-fit: cover;">
                                        <h5 class="card-title fw-bold text-dark">{{ other.profile.full_name|default:other.username }}</h5>
                                        <p class="text-muted small"><i class="fa-solid fa-phone"></i> {{ other.profile.mobile_number|default:"Hidden" }}</p>
                                    {% endwith %}
                                {% endif %}
                                <a href="#" class="btn btn-outline-success w-100 rounded-pill"><i class="fa-solid fa-comment"></i> Message</a>
                            </div>
                        </div>
                    </div>
                    {% empty %}
                    <div class="col-12 text-center text-muted py-5">
                        <i class="fa-solid fa-heart-crack fa-3x mb-3 text-secondary"></i>
                        <p>No connections yet.</p>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
        </div>
    </div>
"""
    
    # We will replace the container content with our new tabs UI.
    req_html = re.sub(
        r'<h2 class="section-title mb-4">.*?{% endfor %}\s*</div>',
        tabs_html.strip(),
        req_html,
        flags=re.DOTALL
    )
    with open(req_filepath, 'w', encoding='utf-8') as f:
        f.write(req_html)
    print("Updated requests.html")

