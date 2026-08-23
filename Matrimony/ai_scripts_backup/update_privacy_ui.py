import os

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web\my_profile_data.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add a Privacy Settings card in my_profile_data.html
if 'Privacy & Security' not in content:
    privacy_card = '''
    <div class="card mb-4" style="border: none; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);">
        <div class="card-header" style="background: white; border-bottom: 1px solid #f1f5f9; padding: 20px;">
            <h5 class="mb-0" style="font-weight: 700; color: #1e293b;"><i class="fa-solid fa-shield-halved" style="color: #e94057; margin-right: 10px;"></i> Privacy & Security</h5>
        </div>
        <div class="card-body" style="padding: 25px;">
            <div class="form-check form-switch" style="display: flex; align-items: center; gap: 15px;">
                <input class="form-check-input" type="checkbox" id="privacyBlurToggle" onchange="togglePrivacyBlur(this.checked)" {% if profile.privacy_blur %}checked{% endif %} style="width: 50px; height: 25px;">
                <label class="form-check-label" for="privacyBlurToggle" style="font-weight: 600; font-size: 16px; color: #475569;">Blur my photos for non-premium members</label>
            </div>
            <p class="text-muted mt-2" style="font-size: 13px; margin-left: 65px;">If enabled, your profile photos will appear blurred to free members. Only paid members or connections will see your clear photos.</p>
        </div>
    </div>
    
    <script>
    function togglePrivacyBlur(isChecked) {
        fetch('/profiles/update_privacy/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({privacy_blur: isChecked})
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === 'success') {
                // Settings saved silently
            }
        });
    }
    </script>
    '''
    # We will inject this right before the main container ends or before a known section
    if '<!-- Personal Details Card -->' in content:
        content = content.replace('<!-- Personal Details Card -->', privacy_card + '\n<!-- Personal Details Card -->')
    else:
        # Just append it before closing main
        content = content.replace('</main>', privacy_card + '\n</main>')
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        print('Injected Privacy toggle.')
else:
    print('Privacy toggle already exists.')
