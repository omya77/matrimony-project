import os

template_dir = r"c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web"

old_str = "background: linear-gradient(135deg, var(--rose) 0%, var(--pink) 100%);"
new_str = "background: linear-gradient(135deg, #e94057 0%, #ff5c75 100%);"

for filename in os.listdir(template_dir):
    if not filename.endswith(".html"):
        continue
    filepath = os.path.join(template_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_str in content:
        content = content.replace(old_str, new_str)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed colors in {filename}")
