from django.db import models
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

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=150)
    message = models.TextField(max_length=1000)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
