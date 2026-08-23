from django.db import models

class CounselingQuery(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    topic = models.CharField(max_length=150)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    admin_reply = models.TextField(blank=True, null=True, help_text="Type your reply here. Saving the model will automatically send this reply to the user's email.")
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Query from {self.full_name} on {self.topic}"