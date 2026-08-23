import os
import re

template_dir = r"c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web"

old_age_options = """        <datalist id="pm-age-list">

            <option value="18 - 22">

            <option value="23 - 25">

            <option value="26 - 30">

            <option value="31 - 35">

            <option value="36 - 40">

            <option value="40+">

        </datalist>"""

new_age_options = """        <datalist id="pm-age-list">

            <option value="21 - 25">

            <option value="26 - 30">

            <option value="31 - 35">

            <option value="36 - 40">

            <option value="40+">

        </datalist>"""

for filename in os.listdir(template_dir):
    if not filename.endswith(".html"):
        continue
    filepath = os.path.join(template_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple replace for pm-age-list
    if 'id="pm-age-list"' in content:
        # regex to replace the inner content of datalist
        pattern = r'<datalist id="pm-age-list">.*?</datalist>'
        content = re.sub(pattern, new_age_options, content, flags=re.DOTALL)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated age list in {filename}")

    # Also check matches1.html which has a select for Age
    if filename == "matches1.html":
        # manual replace
        content = content.replace("<option>18 - 22</option>", "<option>21 - 25</option>")
        content = content.replace("<option>23 - 25</option>", "")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated age select in matches1.html")
