import re
import os

css_path = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\static\web\css\chat.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Increase chat container width
css = re.sub(
    r'\.chat-container\s*\{[^}]*\}',
    '''.chat-container {
    display: flex;
    height: calc(100vh - 120px);
    max-width: 1250px;
    width: 95%;
    margin: 20px auto;
    background: var(--chat-panel-bg);
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
    overflow: hidden;
    border: 1px solid var(--chat-border);
}''', css)

# 2. Fix avatar height/aspect-ratio
css = re.sub(
    r'\.contact-avatar\s*\{[^}]*\}',
    '''.contact-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    object-fit: cover;
    aspect-ratio: 1/1;
    margin-right: 15px;
}''', css)

# 3. WhatsApp style bubbles
css = re.sub(
    r'\.message-bubble\s*\{[^}]*\}',
    '''.message-bubble {
    padding: 8px 12px;
    border-radius: 12px;
    font-size: 15px;
    line-height: 1.4;
    position: relative;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    word-wrap: break-word;
    word-break: break-word;
    width: fit-content;
    max-width: 100%;
    display: flex;
    flex-wrap: wrap;
    align-items: flex-end;
    gap: 10px;
}''', css)

css = re.sub(
    r'\.incoming \.message-bubble\s*\{[^}]*\}',
    '''.incoming .message-bubble {
    background: #ffffff;
    color: var(--chat-text);
    border-top-left-radius: 2px;
    align-self: flex-start;
    border: 1px solid var(--chat-border);
}''', css)

css = re.sub(
    r'\.outgoing \.message-bubble\s*\{[^}]*\}',
    '''.outgoing .message-bubble {
    background: linear-gradient(135deg, var(--rose, #e94057), var(--pink, #ff7aa2));
    color: #ffffff;
    border-top-right-radius: 2px;
    align-self: flex-end;
}''', css)

css = re.sub(
    r'\.message-time\s*\{[^}]*\}',
    '''.message-time {
    font-size: 11px;
    color: inherit;
    opacity: 0.8;
    margin-top: 2px;
    display: flex;
    align-items: center;
    gap: 4px;
}''', css)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

# Now modify chat.html
html_path = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web\chat.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Remove dummy messages
start_marker = '<div class="chat-messages">'
end_marker = '<div class="chat-input-area">'
start_idx = html.find(start_marker)
end_idx = html.find(end_marker)
if start_idx != -1 and end_idx != -1:
    html = html[:start_idx + len(start_marker)] + '\n            <!-- Messages will load here -->\n          </div>\n\n          ' + html[end_idx:]

# Fix avatar inline styles which might override css
html = re.sub(
    r'style="width:\s*45px;\s*height:\s*45px;\s*border-radius:\s*50%;\s*object-fit:\s*cover;\s*margin-right:\s*15px;"',
    '',
    html
)

# Put time inside bubble in JS
js_bubble_old = '''<div class="message-bubble">${escapeHTML(msg.message)}</div>
                                <span class="message-time">${formatTime(msg.timestamp)} ${isOutgoing ? \'<i class="fa-solid fa-check" style="color: #10b981"></i>\' : \'\'}</span>'''
js_bubble_new = '''<div class="message-bubble">
                                    <span>${escapeHTML(msg.message)}</span>
                                    <span class="message-time">${formatTime(msg.timestamp)} ${isOutgoing ? \'<i class="fa-solid fa-check-double" style="color: #ffffff"></i>\' : \'\'}</span>
                                </div>'''
html = html.replace(js_bubble_old, js_bubble_new)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print('Updated chat styles and HTML.')
