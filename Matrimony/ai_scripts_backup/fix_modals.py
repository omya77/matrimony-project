import os
import re

template_dir = r"c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web"

global_modals_snippet = """
<!-- Global Profile Modals -->
{% for match in matches %}
    {% include 'web/profile_modal.html' %}
{% endfor %}
</body>
"""

for filename in os.listdir(template_dir):
    if not filename.endswith(".html"):
        continue
    
    # We only care about files that HAVE {% include 'web/profile_modal.html' %} inside the loop
    filepath = os.path.join(template_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if the file has the include
    if "{% include 'web/profile_modal.html' %}" in content:
        # Check if we already appended the global modals snippet
        if "<!-- Global Profile Modals -->" in content:
            continue
            
        # Remove all instances of the inline include
        content = content.replace("{% include 'web/profile_modal.html' %}", "")
        
        # Append to the bottom before </body>
        if "</body>" in content:
            content = content.replace("</body>", global_modals_snippet)
        else:
            content += global_modals_snippet
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed modal stacking in {filename}")
