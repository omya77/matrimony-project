import os

template_dir = r"c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web"

old_btn = 'style="width: 100%; border-radius: 25px; background: #e2e8f0; color: #475569; font-weight: 600;"'
new_btn = 'style="width: 100%; border-radius: 25px; padding: 12px 0; border: none; background: linear-gradient(135deg, var(--rose) 0%, var(--pink) 100%); color: white; font-weight: 600; cursor: pointer; transition: all 0.3s ease; display: inline-flex; justify-content: center; align-items: center;"'

for filename in os.listdir(template_dir):
    if not filename.endswith(".html"):
        continue
    filepath = os.path.join(template_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_btn in content:
        content = content.replace(old_btn, new_btn)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed button style in {filename}")
