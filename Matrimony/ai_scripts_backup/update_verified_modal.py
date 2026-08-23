filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web\verified_profiles.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

modal_btn_target = '''<button
                        class="btn flex-grow-1 send-interest-action"
                        data-user-id="{{ match.user.id }}"
                        id="modal-send-btn"
                        style="
                          background: linear-gradient(135deg, #10b981, #34d399);
                          color: white;
                          border-radius: 25px;
                          font-weight: 600;
                          padding: 12px;
                        "
                      >
                        <i class="fa-solid fa-heart"></i> Send Interest
                      </button>'''

modal_btn_replacement = '''
                      {% if int_status == 'accepted' %}
                        <button class="btn flex-grow-1" style="background: linear-gradient(135deg, #10b981, #34d399); color: white; border-radius: 25px; font-weight: 600; padding: 12px; pointer-events: none;"><i class="fa-solid fa-check"></i> Connected</button>
                      {% elif int_status == 'pending_sent' %}
                        <button class="btn flex-grow-1" style="background: linear-gradient(135deg, #64748b, #94a3b8); color: white; border-radius: 25px; font-weight: 600; padding: 12px; pointer-events: none;"><i class="fa-solid fa-clock"></i> Request Sent</button>
                      {% elif int_status == 'pending_received' %}
                        <a href="/interactions/requests/" class="btn flex-grow-1 text-decoration-none" style="background: linear-gradient(135deg, #3b82f6, #60a5fa); color: white; border-radius: 25px; font-weight: 600; padding: 12px; text-align: center;"><i class="fa-solid fa-reply"></i> Respond</a>
                      {% else %}
                        <button class="btn flex-grow-1 send-interest-action" data-user-id="{{ match.user.id }}" id="modal-send-btn" onclick="sendInterest({{ match.user.id }}, this)" style="background: linear-gradient(135deg, #10b981, #34d399); color: white; border-radius: 25px; font-weight: 600; padding: 12px;"><i class="fa-solid fa-heart"></i> Send Interest</button>
                      {% endif %}
'''
content = content.replace(modal_btn_target, modal_btn_replacement)

modal_chat_target = '''<button
                        class="btn flex-grow-1 open-chat-action"
                        style="
                          background: linear-gradient(135deg, #d4af37, #ffcc70);
                          color: black;
                          border-radius: 25px;
                          font-weight: 600;
                          padding: 12px;
                        "
                      >
                        <i class="fa-solid fa-comment-dots"></i> Chat Now
                      </button>'''

modal_chat_replacement = '''
                      {% if int_status == 'accepted' %}
                        <a href="/interactions/chat/" class="btn flex-grow-1 open-chat-action text-decoration-none" style="background: linear-gradient(135deg, #d4af37, #ffcc70); color: black; border-radius: 25px; font-weight: 600; padding: 12px; text-align: center;"><i class="fa-solid fa-comment-dots"></i> Chat Now</a>
                      {% else %}
                        <button class="btn flex-grow-1 text-decoration-none" onclick="alert('You can only chat with users who are connected with you. Send an interest request first!');" style="background: #e2e8f0; color: #64748b; border-radius: 25px; font-weight: 600; padding: 12px; text-align: center; border: none;"><i class="fa-solid fa-lock"></i> Chat</button>
                      {% endif %}
'''
content = content.replace(modal_chat_target, modal_chat_replacement)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated modal buttons in verified_profiles.html')
