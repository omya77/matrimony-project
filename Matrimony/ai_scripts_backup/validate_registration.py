import re

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web\registration.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# firstName
old_fn = '''<input
                    type="text"
                    id="firstName"
                    class="form-control"
                    placeholder="First Name"
                    required
                  />'''
new_fn = '''<input type="text" id="firstName" class="form-control" placeholder="First Name" required maxlength="50" pattern="[A-Za-z ]+" title="Only alphabets and spaces allowed" />'''
content = content.replace(old_fn, new_fn)

# lastName
old_ln = '''<input
                    type="text"
                    id="lastName"
                    class="form-control"
                    placeholder="Last Name"
                    required
                  />'''
new_ln = '''<input type="text" id="lastName" class="form-control" placeholder="Last Name" required maxlength="50" pattern="[A-Za-z ]+" title="Only alphabets and spaces allowed" />'''
content = content.replace(old_ln, new_ln)

# mobileInput
old_mob = '''<input
                    type="tel"
                    id="mobileInput"
                    class="form-control"
                    placeholder="Mobile Number"
                    required
                  />'''
new_mob = '''<input type="tel" id="mobileInput" class="form-control" placeholder="Mobile Number" required minlength="10" maxlength="10" oninput="this.value = this.value.replace(/[^0-9]/g, '');" title="Exactly 10 digits allowed" />'''
content = content.replace(old_mob, new_mob)

# emailInput
old_email = '''<input
                      type="email"
                      id="emailInput"
                      class="form-control"
                      placeholder="Email Address"
                      required
                    />'''
new_email = '''<input type="email" id="emailInput" class="form-control" placeholder="Email Address" required maxlength="100" />'''
content = content.replace(old_email, new_email)

# passwordInput
old_pass = '''<input
                      type="password"
                      id="passwordInput"
                      class="form-control"
                      placeholder="Create Password"
                      required
                    />'''
new_pass = '''<input type="password" id="passwordInput" class="form-control" placeholder="Create Password" required minlength="8" maxlength="50" title="Password must be at least 8 characters" />'''
content = content.replace(old_pass, new_pass)

# confirmPassword
old_cpass = '''<input
                      type="password"
                      id="confirmPassword"
                      class="form-control"
                      placeholder="Confirm Password"
                      required
                    />'''
new_cpass = '''<input type="password" id="confirmPassword" class="form-control" placeholder="Confirm Password" required minlength="8" maxlength="50" title="Must match password" />'''
content = content.replace(old_cpass, new_cpass)

# otp fields
content = content.replace('<input type="text" class="otp-field" id="otp1" maxlength="1" />', '<input type="text" class="otp-field" id="otp1" maxlength="1" oninput="this.value = this.value.replace(/[^0-9]/g, \'\');" />')
content = content.replace('<input type="text" class="otp-field" id="otp2" maxlength="1" />', '<input type="text" class="otp-field" id="otp2" maxlength="1" oninput="this.value = this.value.replace(/[^0-9]/g, \'\');" />')
content = content.replace('<input type="text" class="otp-field" id="otp3" maxlength="1" />', '<input type="text" class="otp-field" id="otp3" maxlength="1" oninput="this.value = this.value.replace(/[^0-9]/g, \'\');" />')
content = content.replace('<input type="text" class="otp-field" id="otp4" maxlength="1" />', '<input type="text" class="otp-field" id="otp4" maxlength="1" oninput="this.value = this.value.replace(/[^0-9]/g, \'\');" />')

# idInput in OTP step
old_id = '''<input
                      type="text"
                      id="idInput"
                      class="form-control"
                      placeholder="Email / Mobile"
                      required
                    />'''
new_id = '''<input type="text" id="idInput" class="form-control" placeholder="Email / Mobile" required maxlength="100" />'''
content = content.replace(old_id, new_id)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated registration.html")
