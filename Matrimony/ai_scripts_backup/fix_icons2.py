import os
import re

html_dir = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web'

for filename in os.listdir(html_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(html_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = False
        
        # 1. Saved Profiles - replace whatever icon exists with fa-bookmark
        # Find exactly: href="/profiles/saved-profiles/"
        # We want to make sure it has an icon
        parts = content.split('href="/profiles/saved-profiles/"')
        if len(parts) > 1:
            for i in range(1, len(parts)):
                if 'Saved Profiles</a' in parts[i]:
                    # Remove any existing icon in that chunk
                    chunk = parts[i][:parts[i].find('Saved Profiles</a')]
                    chunk_no_icon = re.sub(r'<i[^>]*>.*?</i>', '', chunk, flags=re.DOTALL)
                    # Add our icon
                    chunk_no_icon = chunk_no_icon.replace('>', '><i class="fa-solid fa-bookmark" style="color: #e94057; margin-right: 8px;"></i> ', 1)
                    parts[i] = chunk_no_icon + parts[i][parts[i].find('Saved Profiles</a'):]
            content = 'href="/profiles/saved-profiles/"'.join(parts)
            modified = True

        # 2. Verified Profiles
        parts = content.split('href="/profiles/verified-profiles/"')
        if len(parts) > 1:
            for i in range(1, len(parts)):
                if 'Verified Profiles</a' in parts[i]:
                    chunk = parts[i][:parts[i].find('Verified Profiles</a')]
                    chunk_no_icon = re.sub(r'<i[^>]*>.*?</i>', '', chunk, flags=re.DOTALL)
                    chunk_no_icon = chunk_no_icon.replace('>', '><i class="fa-solid fa-user-shield" style="color: #e94057; margin-right: 8px;"></i> ', 1)
                    parts[i] = chunk_no_icon + parts[i][parts[i].find('Verified Profiles</a'):]
            content = 'href="/profiles/verified-profiles/"'.join(parts)
            modified = True
            
        # 3. Featured Grooms
        parts = content.split('href="/interactions/featured/grooms/"')
        if len(parts) > 1:
            for i in range(1, len(parts)):
                if 'Featured Grooms</a' in parts[i]:
                    chunk = parts[i][:parts[i].find('Featured Grooms</a')]
                    chunk_no_icon = re.sub(r'<i[^>]*>.*?</i>', '', chunk, flags=re.DOTALL)
                    chunk_no_icon = chunk_no_icon.replace('>', '><i class="fa-solid fa-person" style="color: #e94057; margin-right: 8px;"></i> ', 1)
                    parts[i] = chunk_no_icon + parts[i][parts[i].find('Featured Grooms</a'):]
            content = 'href="/interactions/featured/grooms/"'.join(parts)
            modified = True
            
        # 4. Featured Brides
        parts = content.split('href="/interactions/featured/brides/"')
        if len(parts) > 1:
            for i in range(1, len(parts)):
                if 'Featured Brides</a' in parts[i]:
                    chunk = parts[i][:parts[i].find('Featured Brides</a')]
                    chunk_no_icon = re.sub(r'<i[^>]*>.*?</i>', '', chunk, flags=re.DOTALL)
                    chunk_no_icon = chunk_no_icon.replace('>', '><i class="fa-solid fa-person-dress" style="color: #e94057; margin-right: 8px;"></i> ', 1)
                    parts[i] = chunk_no_icon + parts[i][parts[i].find('Featured Brides</a'):]
            content = 'href="/interactions/featured/brides/"'.join(parts)
            modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated icons in {filename}")
