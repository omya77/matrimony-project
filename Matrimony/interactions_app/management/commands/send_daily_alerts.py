from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import User
from interactions_app.models import InterestRequest, ChatMessage
from profiles_app.models import Profile

class Command(BaseCommand):
    help = 'Sends daily email alerts to users who have unread messages or pending requests.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting offline email alert engine...')
        
        # Look back 24 hours
        yesterday = timezone.now() - timedelta(hours=24)
        
        # Get users who have email_notifications enabled
        users_with_alerts = User.objects.filter(profile__email_notifications=True)
        
        emails_sent = 0
        
        for user in users_with_alerts:
            if not user.email:
                continue
                
            # Count unread requests in last 24h
            unread_requests = InterestRequest.objects.filter(
                receiver=user, 
                status='pending', 
                is_viewed=False,
                created_at__gte=yesterday
            ).count()
            
            # Count unread messages in last 24h
            unread_messages = ChatMessage.objects.filter(
                receiver=user, 
                is_read=False,
                timestamp__gte=yesterday
            ).count()
            
            if unread_requests > 0 or unread_messages > 0:
                self.send_alert_email(user, unread_requests, unread_messages)
                emails_sent += 1
                
        self.stdout.write(self.style.SUCCESS(f'Successfully sent {emails_sent} email alerts!'))

    def send_alert_email(self, user, req_count, msg_count):
        subject = 'You have new activity on ForeverBond!'
        
        message_body = f"Hello {user.profile.full_name or user.username},\n\n"
        message_body += "You have new activity waiting for you on your ForeverBond account.\n\n"
        
        if req_count > 0:
            message_body += f"- You have {req_count} new match request(s).\n"
        if msg_count > 0:
            message_body += f"- You have {msg_count} new unread message(s).\n"
            
        message_body += "\nLogin now to check your dashboard: http://localhost:8000/interactions/matches/today/\n\n"
        message_body += "Best regards,\nThe ForeverBond Team\n"
        message_body += "\n(You received this because your Email Notifications are turned ON in Settings)."
        
        try:
            send_mail(
                subject,
                message_body,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to send email to {user.email}: {str(e)}"))

