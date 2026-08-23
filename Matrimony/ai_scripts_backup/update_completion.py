import re

for filename in ['Template/web/my_profile.html', 'Template/web/my_profile_data.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace hardcoded 85% width and aria-valuenow
    content = re.sub(
        r'<div class="progress-bar" role="progressbar" style="width: \d+%;(.*?)aria-valuenow="\d+"(.*?)></div>',
        r'<div class="progress-bar" role="progressbar" style="width: {{ request.user.profile.completion_percentage }}%;\1aria-valuenow="{{ request.user.profile.completion_percentage }}"\2></div>',
        content
    )

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated completion percentage in profiles")
