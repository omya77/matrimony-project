import os
import re

html_dir = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web'

# 1. Update contact.html
filepath = os.path.join(html_dir, 'contact.html')
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# contactPhone
content = re.sub(
    r'<input type="tel" id="contactPhone" placeholder="Phone Number[^"]*" pattern="[^"]*" title="[^"]*" required />',
    r'<input type="tel" id="contactPhone" placeholder="Phone Number (10 digits)" required minlength="10" maxlength="10" oninput="this.value = this.value.replace(/[^0-9]/g, \'\');" />',
    content
)
# contactName
content = re.sub(
    r'<input type="text" id="contactName" placeholder="Full Name" required />',
    r'<input type="text" id="contactName" placeholder="Full Name" required maxlength="100" pattern="[A-Za-z ]+" title="Only alphabets and spaces allowed" />',
    content
)
# contactEmail
content = re.sub(
    r'<input type="email" id="contactEmail" placeholder="Email Address" required />',
    r'<input type="email" id="contactEmail" placeholder="Email Address" required maxlength="100" />',
    content
)
# contactSubject
content = re.sub(
    r'<input type="text" id="contactSubject" placeholder="Subject" required />',
    r'<input type="text" id="contactSubject" placeholder="Subject" required maxlength="150" />',
    content
)
# contactMessage
content = re.sub(
    r'<textarea rows="7" id="contactMessage" placeholder="Message Details\.\.\." required></textarea>',
    r'<textarea rows="7" id="contactMessage" placeholder="Message Details..." required maxlength="1000"></textarea>',
    content
)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)


# 2. Update login.html
filepath = os.path.join(html_dir, 'login.html')
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '<input type="text" id="loginEmail" class="form-control" placeholder="Mobile Number or Email" required />',
    '<input type="text" id="loginEmail" class="form-control" placeholder="Mobile Number or Email" required maxlength="100" />'
)
content = content.replace(
    '<input type="password" id="loginPassword" class="form-control" placeholder="Password" required />',
    '<input type="password" id="loginPassword" class="form-control" placeholder="Password" required maxlength="50" />'
)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)


# 3. Update forgot_password.html
filepath = os.path.join(html_dir, 'forgot_password.html')
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '<input type="email" name="email" class="form-control" placeholder="Enter your registered email" required>',
    '<input type="email" name="email" class="form-control" placeholder="Enter your registered email" required maxlength="100">'
)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated contact, login, and forgot_password htmls")
