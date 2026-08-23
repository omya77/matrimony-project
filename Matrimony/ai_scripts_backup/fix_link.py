import glob

for f in glob.glob('Template/web/*.html'):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        new_content = content.replace(
            '<a href="/profiles/personal/" class="hover-scale" style="display: block;">',
            '<a href="/profiles/my-profile-data/" class="hover-scale" style="display: block;">'
        )
        
        if new_content != content:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Updated {f}")
    except Exception as e:
        pass
