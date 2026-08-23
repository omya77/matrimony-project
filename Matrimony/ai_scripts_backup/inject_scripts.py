import os

template_dir = 'Template'
scripts_to_inject = """    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/web/js/navbar.js"></script>
    <script src="/static/web/js/global-interactions.js"></script>
"""

for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'bootstrap.bundle.min.js' not in content:
                if '</body>' in content:
                    content = content.replace('</body>', scripts_to_inject + '  </body>')
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f'Injected scripts into {filepath}')
