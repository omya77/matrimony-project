import os

filepath = r'c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\profiles_app\models.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

if 'class KYCDocument' not in content:
    kyc_code = '''
class KYCDocument(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='kyc')
    document_type = models.CharField(max_length=50, choices=(('Aadhar', 'Aadhar Card'), ('PAN', 'PAN Card'), ('Passport', 'Passport')))
    document_file = models.FileField(upload_to='kyc_documents/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.document_type} ({self.status})"
'''
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(kyc_code)
    print('Added KYCDocument model')
