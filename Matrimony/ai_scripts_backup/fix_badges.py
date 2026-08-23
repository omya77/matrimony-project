import re

filepath_main = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web\navbar.html'
with open(filepath_main, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace hardcoded messages (Desktop)
old_msg_d = '''<span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-primary" style="font-size: 9px; padding: 3px 5px;">5</span>'''
new_msg_d = '''{% if unread_messages_count > 0 %}<span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-primary" style="font-size: 9px; padding: 3px 5px;">{{ unread_messages_count }}</span>{% endif %}'''
content = content.replace(old_msg_d, new_msg_d)

# Replace hardcoded messages (Mobile)
old_msg_m = '''<span class="badge rounded-pill bg-primary" style="font-size: 11px;">5</span>'''
new_msg_m = '''{% if unread_messages_count > 0 %}<span class="badge rounded-pill bg-primary" style="font-size: 11px;">{{ unread_messages_count }}</span>{% endif %}'''
content = content.replace(old_msg_m, new_msg_m)

with open(filepath_main, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated navbar.html")

# Now secondary_navbar.html - check the mobile trigger cluster
filepath_sec = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web\secondary_navbar.html'
with open(filepath_sec, 'r', encoding='utf-8') as f:
    content2 = f.read()

# Mobile triggers hardcoded 2 (requests) and 5 (messages)
old_mob_triggers = '''            <!-- Mobile Right Trigger Cluster -->
            <div class="d-flex align-items-center gap-3 d-lg-none">
              <a href="/interactions/requests/" class="text-decoration-none position-relative d-inline-block py-1">
                <i class="fa-solid fa-heart" style="font-size: 18px; color: #e94057;"></i>
              <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" style="font-size: 8px; padding: 2px 4px; background-color: #e94057 !important;">2</span>
              </a>
              <a href="/interactions/chat/" class="text-decoration-none position-relative d-inline-block py-1">
                <i class="fa-brands fa-facebook-messenger" style="font-size: 18px; color: #64748b;"></i>
              <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-primary" style="font-size: 8px; padding: 2px 4px;">5</span>
              </a>'''

new_mob_triggers = '''            <!-- Mobile Right Trigger Cluster -->
            <div class="d-flex align-items-center gap-3 d-lg-none">
              <a href="/interactions/requests/" class="text-decoration-none position-relative d-inline-block py-1">
                <i class="fa-solid fa-heart" style="font-size: 18px; color: #e94057;"></i>
                {% if unread_requests_count > 0 %}
                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" style="font-size: 8px; padding: 2px 4px; background-color: #e94057 !important;">{{ unread_requests_count }}</span>
                {% endif %}
              </a>
              <a href="/interactions/chat/" class="text-decoration-none position-relative d-inline-block py-1">
                <i class="fa-brands fa-facebook-messenger" style="font-size: 18px; color: #64748b;"></i>
                {% if unread_messages_count > 0 %}
                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-primary" style="font-size: 8px; padding: 2px 4px;">{{ unread_messages_count }}</span>
                {% endif %}
              </a>'''
content2 = content2.replace(old_mob_triggers, new_mob_triggers)

# The other one around line 353
old_extra = '''              <!-- Requests & Chat -->
              <a href="/interactions/requests/" class="text-decoration-none position-relative hover-scale d-inline-block py-1" title="Requests & Connections">
                <i class="fa-solid fa-heart" style="font-size: 20px; color: #e94057;"></i>
              <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" style="font-size: 9px; padding: 3px 5px; background-color: #e94057 !important;">2</span>
              </a>
              <a href="/interactions/chat/" class="text-decoration-none position-relative hover-scale d-inline-block py-1" title="Messages">
                <i class="fa-brands fa-facebook-messenger" style="font-size: 20px; color: #64748b;"></i>
              <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-primary" style="font-size: 9px; padding: 3px 5px;">5</span>
              </a>'''

new_extra = '''              <!-- Requests & Chat -->
              <a href="/interactions/requests/" class="text-decoration-none position-relative hover-scale d-inline-block py-1" title="Requests & Connections">
                <i class="fa-solid fa-heart" style="font-size: 20px; color: #e94057;"></i>
                {% if unread_requests_count > 0 %}
                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" style="font-size: 9px; padding: 3px 5px; background-color: #e94057 !important;">{{ unread_requests_count }}</span>
                {% endif %}
              </a>
              <a href="/interactions/chat/" class="text-decoration-none position-relative hover-scale d-inline-block py-1" title="Messages">
                <i class="fa-brands fa-facebook-messenger" style="font-size: 20px; color: #64748b;"></i>
                {% if unread_messages_count > 0 %}
                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-primary" style="font-size: 9px; padding: 3px 5px;">{{ unread_messages_count }}</span>
                {% endif %}
              </a>'''
content2 = content2.replace(old_extra, new_extra)

with open(filepath_sec, 'w', encoding='utf-8') as f:
    f.write(content2)
print("Updated secondary_navbar.html")
