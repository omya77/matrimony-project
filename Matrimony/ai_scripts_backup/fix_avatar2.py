import glob
import re

pattern2 = re.compile(
    r'(<div\s+class="dropdown\s+custom-user-avatar-dropdown\s+position-relative">)\s*'
    r'<a[^>]+href="/profiles/personal/"[^>]*>\s*'
    r'(<div\s+class="position-relative"[^>]*>.*?</span>\s*</div>)\s*'
    r'(<div[^>]+class="[^"]*d-flex\s+flex-column\s+text-start\s+justify-content-center[^"]*"[^>]*>.*?</div>)\s*'
    r'</a>',
    re.DOTALL
)

def repl(match):
    div_start = match.group(1).replace('position-relative"', 'position-relative d-flex align-items-center gap-2"')
    img_div = match.group(2)
    text_div = match.group(3)
    
    return f"""{div_start}
  <a href="/profiles/personal/" class="hover-scale" style="display: block;">
    {img_div}
  </a>
  <a href="javascript:void(0)" class="text-decoration-none dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false" role="button" style="cursor: pointer;">
    {text_div}
  </a>"""

count_total = 0
for f in glob.glob('Template/web/*.html'):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        new_content, count = pattern2.subn(repl, content)
        
        if count > 0:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Updated {f}")
            count_total += 1
    except Exception as e:
        print(f"Error {f}: {e}")
        
print(f"Total updated: {count_total}")
