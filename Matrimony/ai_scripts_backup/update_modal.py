import os
import re

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web\profile_modal.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add Report and Block buttons to modal footer
if '<!-- Modal Footer -->' in content:
    buttons = '''
        <div style="display: flex; gap: 10px;">
            <button type="button" class="btn btn-outline-danger rounded-pill" onclick="reportUser({{ match.user.id }})"><i class="fa-solid fa-flag"></i> Report</button>
            <button type="button" class="btn btn-outline-dark rounded-pill" onclick="blockUser({{ match.user.id }})"><i class="fa-solid fa-ban"></i> Block</button>
        </div>
'''
    content = content.replace('<!-- Modal Footer -->', '<!-- Modal Footer -->\n' + buttons)

# Replace the photo display with privacy blur logic
# The original modal might have a photo like <img src="{{ match.profile.photo.url }}"
# Let's just inject the blur CSS if it isn't there
if '.privacy-blur' not in content:
    css = '''
<style>
.privacy-blur {
    filter: blur(15px);
    pointer-events: none;
}
.blur-overlay {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    text-align: center;
    background: rgba(0,0,0,0.6);
    padding: 10px;
    border-radius: 10px;
    font-weight: bold;
    z-index: 10;
}
</style>
'''
    content = css + content
    
    # Attempt to replace the photo class to conditionally add privacy-blur
    content = content.replace('class="img-fluid profile-image"', 
                              'class="img-fluid profile-image {% if match.profile.privacy_blur and not request.user.profile.payment_status == \'Paid\' %}privacy-blur{% endif %}"')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated profile_modal.html")
