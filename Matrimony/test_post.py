import requests

url = 'http://localhost:8000/contact/'
data = {
    'name': 'Test User',
    'email': 'test@example.com',
    'phone': '1234567890',
    'subject': 'Test Subject',
    'message': 'This is a test message.'
}

# The backend requires CSRF token, but since we are not using a session with CSRF cookie, it might fail.
# Let's see what response we get.
try:
    response = requests.post(url, data=data)
    print("Status Code:", response.status_code)
except Exception as e:
    print("Error:", e)
