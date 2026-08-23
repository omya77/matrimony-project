import os

for root, dirs, files in os.walk('.'):
    if 'env' in root or '__pycache__' in root: continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if 'mobile' in content.lower():
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'maxlength' in line.lower() and ('8' in line or '10' in line):
                            print(f"{filepath}:{i+1}: {line.strip()}")
