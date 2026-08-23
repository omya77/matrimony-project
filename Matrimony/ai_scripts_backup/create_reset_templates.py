import os

tpl_dir = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\admin_panel'

base_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ForeverBond Admin Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #9F2B68;
            --primary-light: #C15483;
            --secondary: #D4AF37;
            --bg-main: #FDFBF7;
        }
        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-main);
            background-image: 
                radial-gradient(at 0% 0%, rgba(159, 43, 104, 0.08) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(212, 175, 55, 0.08) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(159, 43, 104, 0.05) 0px, transparent 50%);
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }
        .login-card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.6);
            border-radius: 24px;
            box-shadow: 0 20px 50px -10px rgba(159, 43, 104, 0.15);
            width: 100%;
            max-width: 450px;
            padding: 50px 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .login-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 5px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
        }
        .brand { margin-bottom: 30px; }
        .brand i { color: var(--primary); font-size: 3rem; margin-bottom: 10px; }
        .brand h1 { font-family: 'Playfair Display', serif; color: var(--primary); font-size: 2rem; margin: 0; }
        .brand p { color: #837277; font-size: 0.9rem; margin-top: 5px; text-transform: uppercase; letter-spacing: 2px; }
        
        .desc-text { color: #2C1E22; font-size: 0.95rem; line-height: 1.5; margin-bottom: 25px; }
        
        .input-group { margin-bottom: 25px; text-align: left; position: relative; }
        .input-group label { display: block; margin-bottom: 8px; font-size: 0.85rem; font-weight: 600; color: #2C1E22; text-transform: uppercase; letter-spacing: 0.5px; }
        .input-group input { width: 100%; padding: 15px 20px 15px 45px; border: 1px solid rgba(159, 43, 104, 0.2); border-radius: 12px; font-size: 1rem; font-family: 'Outfit', sans-serif; background: rgba(255, 255, 255, 0.9); outline: none; transition: all 0.3s; box-sizing: border-box; }
        .input-group input:focus { border-color: var(--primary); box-shadow: 0 0 0 4px rgba(159, 43, 104, 0.1); }
        .input-group i { position: absolute; bottom: 16px; left: 18px; color: var(--primary); font-size: 1.1rem; }
        
        .login-btn { width: 100%; padding: 16px; background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%); color: white; border: none; border-radius: 12px; font-size: 1.05rem; font-weight: 700; font-family: 'Outfit', sans-serif; cursor: pointer; transition: all 0.3s; box-shadow: 0 8px 20px rgba(159, 43, 104, 0.2); display: inline-block; text-decoration: none; box-sizing: border-box; }
        .login-btn:hover { transform: translateY(-2px); box-shadow: 0 12px 25px rgba(159, 43, 104, 0.3); color: white; }
        
        .back-link { display: block; margin-top: 20px; font-size: 0.9rem; color: #837277; text-decoration: none; font-weight: 500; transition: color 0.3s; }
        .back-link:hover { color: var(--primary); }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="brand">
            <i class="fa-solid fa-key"></i>
            <h1>{TITLE}</h1>
            <p>{SUBTITLE}</p>
        </div>
        {CONTENT}
    </div>
</body>
</html>'''

templates = {
    'password_reset_form.html': {
        'title': 'Reset Password',
        'subtitle': 'Admin Account Recovery',
        'content': '''
        <p class="desc-text">Enter your admin email address below and we'll send you a secure link to reset your password.</p>
        <form method="POST">
            {% csrf_token %}
            <div class="input-group">
                <label>Admin Email Address</label>
                <i class="fa-solid fa-envelope"></i>
                <input type="email" name="email" placeholder="e.g. admin@foreverbond.com" required>
            </div>
            <button type="submit" class="login-btn">Send Reset Link</button>
        </form>
        <a href="{% url 'admin_login' %}" class="back-link"><i class="fa-solid fa-arrow-left"></i> Back to Login</a>
        '''
    },
    'password_reset_done.html': {
        'title': 'Email Sent',
        'subtitle': 'Check Your Inbox',
        'content': '''
        <div style="font-size: 4rem; color: #059669; margin-bottom: 20px;">
            <i class="fa-solid fa-circle-check"></i>
        </div>
        <p class="desc-text">We've emailed you instructions for setting your password, if an account exists with the email you entered.</p>
        <p class="desc-text" style="font-size: 0.85rem; color: #837277;">You should receive them shortly. If you don't receive an email, please make sure you've entered the address you registered with.</p>
        <br>
        <a href="{% url 'admin_login' %}" class="login-btn">Return to Login</a>
        '''
    },
    'password_reset_confirm.html': {
        'title': 'Set New Password',
        'subtitle': 'Secure Your Account',
        'content': '''
        <p class="desc-text">Please enter your new password twice so we can verify you typed it in correctly.</p>
        <form method="POST">
            {% csrf_token %}
            <div class="input-group">
                <label>New Password</label>
                <i class="fa-solid fa-lock"></i>
                <input type="password" name="new_password1" placeholder="Enter new password" required>
            </div>
            <div class="input-group">
                <label>Confirm Password</label>
                <i class="fa-solid fa-lock"></i>
                <input type="password" name="new_password2" placeholder="Confirm new password" required>
            </div>
            <button type="submit" class="login-btn">Update Password</button>
        </form>
        '''
    },
    'password_reset_complete.html': {
        'title': 'Password Updated',
        'subtitle': 'Success',
        'content': '''
        <div style="font-size: 4rem; color: #059669; margin-bottom: 20px;">
            <i class="fa-solid fa-shield-check"></i>
        </div>
        <p class="desc-text">Your password has been set successfully. You may go ahead and log in now.</p>
        <br>
        <a href="{% url 'admin_login' %}" class="login-btn">Log in to Admin Portal</a>
        '''
    }
}

for filename, data in templates.items():
    content = base_html.replace('{TITLE}', data['title']).replace('{SUBTITLE}', data['subtitle']).replace('{CONTENT}', data['content'])
    with open(os.path.join(tpl_dir, filename), 'w', encoding='utf-8') as f:
        f.write(content)

# Email Templates
email_txt = "Hello,\n\nYou requested a password reset for your ForeverBond Admin account.\n\nPlease click the link below to reset your password:\n{{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}\n\nIf you didn't request this, you can safely ignore this email.\n\nRegards,\nForeverBond Team"
with open(os.path.join(tpl_dir, 'password_reset_email.html'), 'w', encoding='utf-8') as f:
    f.write(email_txt)

with open(os.path.join(tpl_dir, 'password_reset_subject.txt'), 'w', encoding='utf-8') as f:
    f.write("Password Reset Request - ForeverBond")

print("Generated all password reset templates.")
