import os
import re

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web\personal.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix mobile
content = re.sub(
    r'<input type="tel" id="userMobile" class="form-control" placeholder="e\.g\. 9876543210" required maxlength="15" pattern="\^\\\\?[0-9\\\\s\\\\-]\{10,15\}\$"/>',
    r'<input type="tel" id="userMobile" class="form-control" placeholder="e.g. 9876543210" required minlength="10" maxlength="10" oninput="this.value = this.value.replace(/[^0-9]/g, \'\');" />',
    content
)

# And if that regex didn't work exactly, let's just do a string replace:
old_mobile = '''<input type="tel" id="userMobile" class="form-control" placeholder="e.g. 9876543210" required maxlength="15" pattern="^\+?[0-9\s\-]{10,15}$"/>'''
new_mobile = '''<input type="tel" id="userMobile" class="form-control" placeholder="e.g. 9876543210" required minlength="10" maxlength="10" oninput="this.value = this.value.replace(/[^0-9]/g, '');" />'''
content = content.replace(old_mobile, new_mobile)

# Let's also fix prefAgeMin and prefAgeMax to reject anything except numbers
content = content.replace(
    '<input type="number" class="form-control" id="prefAgeMin" placeholder="Min" min="21" max="70" required />',
    '<input type="number" class="form-control" id="prefAgeMin" placeholder="Min" min="21" max="70" required oninput="this.value = this.value.replace(/[^0-9]/g, \'\');" />'
)
content = content.replace(
    '<input type="number" class="form-control" id="prefAgeMax" placeholder="Max" min="21" max="70" required />',
    '<input type="number" class="form-control" id="prefAgeMax" placeholder="Max" min="21" max="70" required oninput="this.value = this.value.replace(/[^0-9]/g, \'\');" />'
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated personal.html")
