import glob

search_str = 'href="javascript:void(0)" class="d-flex align-items-center gap-2 text-decoration-none dropdown-toggle" data-bs-toggle="dropdown"'
replace_str = 'href="/profiles/personal/" class="d-flex align-items-center gap-2 text-decoration-none dropdown-toggle"'

for f in glob.glob('Template/web/*.html'):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        if search_str in content:
            content = content.replace(search_str, replace_str)
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated {f}")
    except Exception as e:
        pass
