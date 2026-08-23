import os

dashboard_path = "Template/web/../admin_panel/dashboard.html"
base_path = "Template/web/../admin_panel/base_admin.html"

with open(dashboard_path, "r", encoding="utf-8") as f:
    dashboard_content = f.read()

# Extract content between <style> and </style> in dashboard.html
start_idx = dashboard_content.find("<style>")
end_idx = dashboard_content.find("</style>")

if start_idx != -1 and end_idx != -1:
    css_content = dashboard_content[start_idx + 7:end_idx]
    
    # Remove the whole <style>...</style> from dashboard (we can leave {% block extra_css %}{% endblock %})
    new_dashboard_content = dashboard_content[:start_idx] + dashboard_content[end_idx + 8:]
    
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(new_dashboard_content)
        
    print("Extracted CSS from dashboard.html")
    
    with open(base_path, "r", encoding="utf-8") as f:
        base_content = f.read()
        
    # Find closing style in base_admin.html
    base_style_end = base_content.find("</style>")
    if base_style_end != -1:
        new_base_content = base_content[:base_style_end] + css_content + "\n" + base_content[base_style_end:]
        with open(base_path, "w", encoding="utf-8") as f:
            f.write(new_base_content)
        print("Injected CSS into base_admin.html")
else:
    print("Could not find <style> tags in dashboard.html")
