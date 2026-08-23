filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web\verified_profiles.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Load tags
if '{% load interaction_tags %}' not in content:
    content = content.replace('{% block content %}', '{% block content %}\n{% load interaction_tags %}')

# We need to inject the int_status variable inside the loop
loop_target = '{% for match in matches %}'
if '{% get_interaction_status request.user match.user as int_status %}' not in content:
    content = content.replace(loop_target, loop_target + '\n              {% get_interaction_status request.user match.user as int_status %}')

# Replace buttons
btn_target = '''<a href="javascript:void(0);" class="btn-primary-custom send-interest-action" onclick="sendInterest({{ match.user.id }}, this);"><i class="fa-solid fa-heart"></i> Send Interest</a>'''
btn_replacement = '''
                    {% if int_status == 'accepted' %}
                      <a href="javascript:void(0);" class="btn-primary-custom" style="background: #10b981; pointer-events: none;"><i class="fa-solid fa-check"></i> Connected</a>
                    {% elif int_status == 'pending_sent' %}
                      <a href="javascript:void(0);" class="btn-primary-custom" style="background: #64748b; pointer-events: none;"><i class="fa-solid fa-clock"></i> Request Sent</a>
                    {% elif int_status == 'pending_received' %}
                      <a href="/interactions/requests/" class="btn-primary-custom" style="background: #3b82f6;"><i class="fa-solid fa-reply"></i> Respond</a>
                    {% else %}
                      <a href="javascript:void(0);" class="btn-primary-custom send-interest-action" onclick="sendInterest({{ match.user.id }}, this);"><i class="fa-solid fa-heart"></i> Send Interest</a>
                    {% endif %}
                    '''
content = content.replace(btn_target, btn_replacement)

chat_target = '''<a href="/interactions/chat/" class="btn-premium-chat open-chat-action"><i class="fa-solid fa-comment-dots"></i> Chat</a>'''
chat_replacement = '''
                        {% if int_status == 'accepted' %}
                          <a href="/interactions/chat/" class="btn-premium-chat"><i class="fa-solid fa-comment-dots"></i> Chat</a>
                        {% else %}
                          <a href="javascript:void(0);" class="btn-premium-chat" onclick="alert('You can only chat with users who are connected with you. Send an interest request first!');" style="background: #e2e8f0; color: #64748b; box-shadow: none;"><i class="fa-solid fa-lock"></i> Chat</a>
                        {% endif %}
                        '''
content = content.replace(chat_target, chat_replacement)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated verified_profiles.html buttons.')
