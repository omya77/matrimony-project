import os

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\Template\web\my_profile_data.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

history_btn = '''
        <div class="card-body" style="padding: 25px;">
            <a href="{% url 'payment_history' %}" class="btn btn-outline-primary rounded-pill mb-3" style="width: 100%;"><i class="fa-solid fa-clock-rotate-left"></i> View Payment History</a>
'''

if 'View Payment History' not in content:
    content = content.replace('<div class="card-body" style="padding: 25px;">', history_btn, 1)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Added payment history link to dashboard.')
