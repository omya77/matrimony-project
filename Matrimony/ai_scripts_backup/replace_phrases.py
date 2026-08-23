import os, fnmatch, re

search_dir = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony'
patterns = ['*.html', '*.py']

for root, dirs, files in os.walk(search_dir):
    if 'migrations' in root or '.git' in root or 'venv' in root or '__pycache__' in root:
        continue
    for pattern in patterns:
        for filename in fnmatch.filter(files, pattern):
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                
                # Replace specific 'ForeverBond' phrases that are visible text
                replacements = [
                    ('Welcome to ForeverBond', 'Welcome to ForeverBond'),
                    ('the ForeverBond portal', 'the ForeverBond portal'),
                    ('ForeverBond Admin', 'ForeverBond Admin'),
                    ('ForeverBond Dashboard', 'ForeverBond Dashboard'),
                    ('Your ForeverBond Profile', 'Your ForeverBond Profile'),
                    ('ForeverBond platform', 'ForeverBond platform'),
                    ('ForeverBond Platform', 'ForeverBond Platform')
                ]
                
                for old_str, new_str in replacements:
                    new_content = new_content.replace(old_str, new_str)
                
                new_content = re.sub(r'>\s*Matrimony\s*<', '>ForeverBond<', new_content)
                new_content = re.sub(r'"ForeverBond"', '"ForeverBond"', new_content)
                new_content = re.sub(r"'ForeverBond'", "'ForeverBond'", new_content)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f'Updated {file_path}')
            except Exception as e:
                pass
print('Done phrases.')
