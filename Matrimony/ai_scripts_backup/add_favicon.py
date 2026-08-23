import os

html_dir = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web'
files = ['dashboard.html', 'external_payment_link.html', 'forgot_password.html']

for filename in files:
    filepath = os.path.join(html_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        if '<head>' in content:
            content = content.replace('<head>', '<head>\n    <link rel="icon" type="image/png" href="/static/web/images/favicon.png">')
            with open(filepath, 'w', encoding='utf-8') as out:
                out.write(content)
            print(f'Added favicon to {filename}')
