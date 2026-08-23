import os
import re

premium_css = """
    <style>
      :root {
        --rose: #e94057;
        --pink: #ff7aa2;
        --glass-bg: rgba(255, 255, 255, 0.85);
        --glass-border: rgba(255, 255, 255, 0.5);
      }
      .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(233, 64, 87, 0.1);
        transition: all 0.3s ease;
      }
      .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(233, 64, 87, 0.2);
      }
      .btn-premium-gradient {
        background: linear-gradient(135deg, var(--rose) 0%, var(--pink) 100%);
        color: #fff;
        border: none;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
      }
      .btn-premium-gradient:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(233, 64, 87, 0.3);
        color: #fff;
      }
      body {
        background: linear-gradient(135deg, #fff0f2 0%, #f1f5f9 100%);
      }
    </style>
"""

# Common function to enhance styling and add send-interest logic
def upgrade_template(filepath, add_interest_js=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'var(--glass-bg)' not in content:
        # Add CSS
        content = content.replace('</head>', premium_css + '\n</head>')
        
        # Upgrade cards
        content = content.replace('class="card profile-card"', 'class="card profile-card glass-card"')
        content = content.replace('class="card shadow-sm', 'class="card glass-card shadow-sm')
        content = content.replace('class="btn btn-danger', 'class="btn btn-premium-gradient')

        # Add Send Interest JS if not present
        if add_interest_js and 'sendInterest' not in content:
            js_script = """
            <script>
            function sendInterest(receiverId, btnElement) {
                btnElement.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending...';
                fetch('/interactions/api/express-interest/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': '{{ csrf_token }}' },
                    body: JSON.stringify({ receiver_id: receiverId })
                }).then(res => res.json()).then(data => {
                    if(data.status === 'pending') {
                        btnElement.innerHTML = '<i class="fa-solid fa-check"></i> Sent';
                        btnElement.disabled = true;
                    } else if (data.status === 'accepted') {
                        btnElement.innerHTML = '<i class="fa-solid fa-heart"></i> Connected';
                        btnElement.disabled = true;
                    } else {
                        alert(data.message);
                        btnElement.innerHTML = '<i class="fa-solid fa-heart"></i> Interest';
                    }
                }).catch(err => {
                    alert('Error sending interest');
                    btnElement.innerHTML = '<i class="fa-solid fa-heart"></i> Interest';
                });
            }
            </script>
            """
            content = content.replace('</body>', js_script + '\n</body>')
            
            # Replace static 'Connect' buttons with the dynamic ones
            # Assuming there's an anchor tag or button for connection
            content = re.sub(
                r'<a href="[^"]*".*?class="btn[^>]*>.*?Connect.*?</a>',
                r'<button onclick="sendInterest({{ match.user.id }}, this)" class="btn btn-premium-gradient w-100"><i class="fa-solid fa-heart"></i> Connect</button>',
                content,
                flags=re.IGNORECASE|re.DOTALL
            )
            content = re.sub(
                r'<button.*?class="btn[^>]*>.*?Connect.*?</button>',
                r'<button onclick="sendInterest({{ match.user.id }}, this)" class="btn btn-premium-gradient w-100"><i class="fa-solid fa-heart"></i> Connect</button>',
                content,
                flags=re.IGNORECASE|re.DOTALL
            )

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Enhanced {filepath}")

# Process search templates
templates = [
    'Template/web/basic_search.html',
    'Template/web/advanced_search.html',
    'Template/web/recomended-matches.html'
]
for t in templates:
    if os.path.exists(t):
        upgrade_template(t)

# Process requests.html
requests_path = 'Template/web/requests.html'
if os.path.exists(requests_path):
    with open(requests_path, 'r', encoding='utf-8') as f:
        req_content = f.read()
    
    if 'var(--glass-bg)' not in req_content:
        req_content = req_content.replace('</head>', premium_css + '\n</head>')
        req_content = req_content.replace('class="card profile-card"', 'class="card profile-card glass-card"')
        
        # Ensure Accept/Reject logic uses the right base URL
        # APIs are at /interactions/api/...
        req_content = req_content.replace('/api/accept-interest/', '/interactions/api/accept-interest/')
        req_content = req_content.replace('/api/reject-interest/', '/interactions/api/reject-interest/')
        
        with open(requests_path, 'w', encoding='utf-8') as f:
            f.write(req_content)
        print(f"Enhanced {requests_path}")
