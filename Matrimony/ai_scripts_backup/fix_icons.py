import os
import re

html_dir = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web'

for filename in os.listdir(html_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(html_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = False
        
        # We need to make sure the dropdown items have the correct icons across all templates
        
        # 1. Featured Brides
        content, n = re.subn(
            r'<a([^>]*?)href="\/interactions\/featured\/brides\/"([^>]*?)>(?:<i[^>]*><\/i>\s*)?Featured Brides<\/a>',
            r'<a\1href="/interactions/featured/brides/"\2><i class="fa-solid fa-person-dress" style="color: #e94057"></i> Featured Brides</a>',
            content, flags=re.IGNORECASE|re.DOTALL
        )
        if n > 0: modified = True
        
        # 2. Featured Grooms
        content, n = re.subn(
            r'<a([^>]*?)href="\/interactions\/featured\/grooms\/"([^>]*?)>(?:<i[^>]*><\/i>\s*)?Featured Grooms<\/a>',
            r'<a\1href="/interactions/featured/grooms/"\2><i class="fa-solid fa-person" style="color: #e94057"></i> Featured Grooms</a>',
            content, flags=re.IGNORECASE|re.DOTALL
        )
        if n > 0: modified = True
        
        # 3. Verified Profiles
        content, n = re.subn(
            r'<a([^>]*?)href="\/profiles\/verified-profiles\/"([^>]*?)>(?:<i[^>]*><\/i>\s*)?Verified Profiles<\/a>',
            r'<a\1href="/profiles/verified-profiles/"\2><i class="fa-solid fa-user-shield" style="color: #e94057"></i> Verified Profiles</a>',
            content, flags=re.IGNORECASE|re.DOTALL
        )
        if n > 0: modified = True
        
        # 4. Saved Profiles (Change folder-heart to bookmark to fix the exclamation mark issue)
        content, n = re.subn(
            r'<a([^>]*?)href="\/profiles\/saved-profiles\/"([^>]*?)>(?:<i[^>]*><\/i>\s*)?Saved Profiles<\/a>',
            r'<a\1href="/profiles/saved-profiles/"\2><i class="fa-solid fa-bookmark" style="color: #e94057"></i> Saved Profiles</a>',
            content, flags=re.IGNORECASE|re.DOTALL
        )
        if n > 0: modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated icons in {filename}")
