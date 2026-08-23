import glob

for f in glob.glob('Template/web/*.html'):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        new_content = content
        
        # Fix email
        if 'misalomkar555@gmail.com' in new_content:
            new_content = new_content.replace('misalomkar555@gmail.com', '{{ request.user.email }}')
            
        # Fix Profile ID
        if 'FB984532' in new_content:
            new_content = new_content.replace('FB984532', '{{ request.user.profile.matrimony_id|default:"Pending" }}')
            
        # Fix alt="Omkar Misal"
        if 'alt="Omkar Misal"' in new_content:
            new_content = new_content.replace('alt="Omkar Misal"', 'alt="{{ request.user.profile.full_name|default:request.user.username }}"')
            
        # Fix alt="Omkar"
        if 'alt="Omkar"' in new_content:
            new_content = new_content.replace('alt="Omkar"', 'alt="{{ request.user.profile.full_name|default:request.user.username }}"')
            
        if new_content != content:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Updated {f}")
    except Exception as e:
        print(e)
