import os

models_code = """from django.db import models
from profiles_app.models import Profile

class SuccessStory(models.Model):
    couple_name = models.CharField(max_length=255)
    wedding_date = models.DateField()
    story_text = models.TextField()
    photo = models.ImageField(upload_to='success_stories/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.couple_name

class PlatformSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.key
"""

with open('admin_panel/models.py', 'w', encoding='utf-8') as f:
    f.write(models_code)
print("Updated admin_panel/models.py")
