from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from profiles_app.models import Profile
from interactions_app.utils import calculate_match_score

class Command(BaseCommand):
    help = 'Sends weekly match emails to all active users with their top 3 recommended matches'

    def handle(self, *args, **options):
        # Fetch all approved profiles
        profiles = Profile.objects.filter(approval_status='Approved')
        
        self.stdout.write(self.style.SUCCESS(f'Found {profiles.count()} profiles. Calculating matches...'))

        emails_sent = 0

        for profile in profiles:
            if not profile.user.email:
                continue

            # We need to find matches for this profile
            # Rules: opposite gender, approved, not themselves
            opposite_gender = 'Female' if profile.gender == 'Male' else 'Male'
            potential_matches = Profile.objects.filter(
                gender=opposite_gender,
                approval_status='Approved'
            ).exclude(id=profile.id)

            scored_matches = []
            for match in potential_matches:
                score = calculate_match_score(profile, match)
                scored_matches.append({
                    'profile': match,
                    'score': score
                })

            # Sort by score descending
            scored_matches.sort(key=lambda x: x['score'], reverse=True)

            # Get top 3
            top_matches = scored_matches[:3]

            if not top_matches:
                continue

            # Render HTML email
            context = {
                'user_profile': profile,
                'top_matches': top_matches,
                'site_url': 'http://127.0.0.1:8000' # In production, this should be from settings
            }

            html_content = render_to_string('web/emails/weekly_matches.html', context)
            text_content = strip_tags(html_content)

            subject = f"Your Top {len(top_matches)} Matrimony Matches of the Week! 💖"
            
            try:
                msg = EmailMultiAlternatives(
                    subject,
                    text_content,
                    'noreply@matrimony.com',
                    [profile.user.email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                emails_sent += 1
                self.stdout.write(f"Sent email to {profile.user.email}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to send email to {profile.user.email}: {e}"))

        self.stdout.write(self.style.SUCCESS(f'Successfully sent {emails_sent} weekly match emails!'))
