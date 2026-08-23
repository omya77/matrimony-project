from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import CounselingQuery

@admin.register(CounselingQuery)
class CounselingQueryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'topic', 'submitted_at', 'is_resolved')
    list_filter = ('is_resolved', 'topic')
    search_fields = ('full_name', 'email', 'topic')
    readonly_fields = ('full_name', 'email', 'topic', 'message', 'submitted_at')
    
    def save_model(self, request, obj, form, change):
        # Check if the admin reply has changed and is not empty
        if change and 'admin_reply' in form.changed_data and obj.admin_reply:
            subject = f"Re: Your Counseling Query about {obj.topic}"
            message = (
                f"Dear {obj.full_name},\n\n"
                f"Thank you for reaching out to us regarding '{obj.topic}'.\n\n"
                f"Counselor's Reply:\n{obj.admin_reply}\n\n"
                f"Best regards,\n"
                f"ForeverBond Counseling Team"
            )
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [obj.email],
                    fail_silently=False,
                )
                obj.is_resolved = True
            except Exception as e:
                # Log or handle the email failure if necessary
                pass
                
        super().save_model(request, obj, form, change)