import re

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web\secondary_navbar.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Messages badge (Desktop)
old_msg_desk = '''              <a href="/interactions/chat/" class="text-decoration-none position-relative hover-scale d-inline-block py-1" title="Messages">
                <i class="fa-brands fa-facebook-messenger" style="font-size: 20px; color: #64748b;"></i>
              <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-primary" style="font-size: 9px; padding: 3px 5px;">5</span>
              </a>'''
new_msg_desk = '''              <a href="/interactions/chat/" class="text-decoration-none position-relative hover-scale d-inline-block py-1" title="Messages">
                <i class="fa-brands fa-facebook-messenger" style="font-size: 20px; color: #64748b;"></i>
                {% if unread_messages_count > 0 %}
                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-primary" style="font-size: 9px; padding: 3px 5px;">{{ unread_messages_count }}</span>
                {% endif %}
              </a>'''
content = content.replace(old_msg_desk, new_msg_desk)

# 2. Update Bell badge (Desktop) and inject dynamic notifications list
old_bell_desk = '''              <div class="dropdown custom-notification-dropdown d-inline-block">
    <a href="javascript:void(0)" class="position-relative text-decoration-none py-1 dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false" role="button">
      <i class="fa-solid fa-bell" style="color: #64748b; font-size: 20px"></i>
      <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" style="font-size: 8px; padding: 3px 5px; background: #e94057 !important;">3</span>
    </a>
    <div class="dropdown-menu dropdown-menu-end shadow-lg border-0 p-0" style="width: 300px; max-width: 85vw; border-radius: 16px; margin-top: 15px; z-index: 1050; overflow: hidden;">
      <div class="p-3 border-bottom d-flex justify-content-between align-items-center" style="background: #f8fafc;">
        <h6 class="m-0" style="font-family: 'Poppins', sans-serif; font-weight: 600; color: #1e293b;">Notifications</h6>
        <span class="badge" style="background: #e94057; font-size: 10px;">3 New</span>
      </div>
      <div class="notification-list" style="max-height: 250px; overflow-y: auto;">
        <a href="javascript:void(0);" class="dropdown-item d-flex align-items-start gap-3 p-3 border-bottom text-wrap" style="white-space: normal;">
          <div class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0" style="width: 40px; height: 40px; background: rgba(233, 64, 87, 0.1); color: #e94057;">
            <i class="fa-solid fa-heart"></i>
          </div>
          <div>
            <p class="m-0" style="font-size: 13px; color: #334155; line-height: 1.4;"><strong>Priya Sharma</strong> accepted your request!</p>
            <small style="color: #94a3b8; font-size: 11px;">2 hours ago</small>
          </div>
        </a>
        <a href="javascript:void(0);" class="dropdown-item d-flex align-items-start gap-3 p-3 text-wrap" style="white-space: normal;">
          <div class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0" style="width: 40px; height: 40px; background: rgba(59, 130, 246, 0.1); color: #3b82f6;">
            <i class="fa-solid fa-message"></i>
          </div>
          <div>
            <p class="m-0" style="font-size: 13px; color: #334155; line-height: 1.4;">You have a new message from <strong>Rahul</strong>.</p>
            <small style="color: #94a3b8; font-size: 11px;">5 hours ago</small>
          </div>
        </a>
      </div>
    </div>
  </div>'''

new_bell_desk = '''              <div class="dropdown custom-notification-dropdown d-inline-block">
    <a href="javascript:void(0)" onclick="markNotificationsRead()" class="position-relative text-decoration-none py-1 dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false" role="button">
      <i class="fa-solid fa-bell" style="color: #64748b; font-size: 20px"></i>
      {% if unread_notifications_count > 0 %}
      <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" style="font-size: 8px; padding: 3px 5px; background: #e94057 !important;" id="notif-badge">{{ unread_notifications_count }}</span>
      {% endif %}
    </a>
    <div class="dropdown-menu dropdown-menu-end shadow-lg border-0 p-0" style="width: 300px; max-width: 85vw; border-radius: 16px; margin-top: 15px; z-index: 1050; overflow: hidden;">
      <div class="p-3 border-bottom d-flex justify-content-between align-items-center" style="background: #f8fafc;">
        <h6 class="m-0" style="font-family: 'Poppins', sans-serif; font-weight: 600; color: #1e293b;">Notifications</h6>
        {% if unread_notifications_count > 0 %}
        <span class="badge" style="background: #e94057; font-size: 10px;" id="notif-text">{{ unread_notifications_count }} New</span>
        {% endif %}
      </div>
      <div class="notification-list" style="max-height: 250px; overflow-y: auto;">
        {% for notif in notifications %}
        <a href="{{ notif.link|default:'javascript:void(0);' }}" class="dropdown-item d-flex align-items-start gap-3 p-3 border-bottom text-wrap" style="white-space: normal; {% if not notif.is_read %}background-color: #f1f5f9;{% endif %}">
          <div class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0" style="width: 40px; height: 40px; background: rgba(233, 64, 87, 0.1); color: #e94057;">
            <i class="fa-solid fa-bell"></i>
          </div>
          <div>
            <p class="m-0" style="font-size: 13px; color: #334155; line-height: 1.4;">{{ notif.message }}</p>
            <small style="color: #94a3b8; font-size: 11px;">{{ notif.created_at|timesince }} ago</small>
          </div>
        </a>
        {% empty %}
        <div class="p-4 text-center">
            <p class="text-muted" style="font-size:13px; margin:0;">No notifications yet.</p>
        </div>
        {% endfor %}
      </div>
    </div>
  </div>'''

# Use regex for replacement to avoid exact whitespace issues
content = re.sub(r'<div class="dropdown custom-notification-dropdown d-inline-block">.*?</div>\s*</div>\s*</div>', new_bell_desk, content, flags=re.DOTALL)

# 3. Update Messages badge (Mobile)
old_msg_mob = '''              <a href="/interactions/chat/" class="nav-link mobile-nav-link d-flex align-items-center justify-content-between" style="font-size:15px; font-weight:700; color:#475569; padding:12px 16px; text-decoration:none;">
                <span class="d-flex align-items-center gap-2"><i class="fa-brands fa-facebook-messenger" style="color:#64748b; width:18px;"></i> MESSAGES</span>
              <span class="badge rounded-pill bg-primary" style="font-size: 11px;">5</span>
              </a>'''
new_msg_mob = '''              <a href="/interactions/chat/" class="nav-link mobile-nav-link d-flex align-items-center justify-content-between" style="font-size:15px; font-weight:700; color:#475569; padding:12px 16px; text-decoration:none;">
                <span class="d-flex align-items-center gap-2"><i class="fa-brands fa-facebook-messenger" style="color:#64748b; width:18px;"></i> MESSAGES</span>
                {% if unread_messages_count > 0 %}
                <span class="badge rounded-pill bg-primary" style="font-size: 11px;">{{ unread_messages_count }}</span>
                {% endif %}
              </a>'''
content = content.replace(old_msg_mob, new_msg_mob)

# 4. Add the JS function for markNotificationsRead
js_code = '''
<script>
function markNotificationsRead() {
    fetch('/interactions/api/mark-notifications-read/', {
        method: 'POST',
        headers: {'X-CSRFToken': '{{ csrf_token }}'}
    }).then(res => {
        if(res.ok) {
            let badge = document.getElementById('notif-badge');
            let text = document.getElementById('notif-text');
            if(badge) badge.style.display = 'none';
            if(text) text.style.display = 'none';
        }
    });
}
</script>
'''
if 'function markNotificationsRead()' not in content:
    content += js_code

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated secondary_navbar.html")
