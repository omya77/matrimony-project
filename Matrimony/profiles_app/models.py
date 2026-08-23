from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    matrimony_id = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    
    # Step 1: Basic Info
    full_name = models.CharField(max_length=150, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True, db_index=True)
    marital_status = models.CharField(max_length=50, blank=True, null=True)
    height = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    is_photo_approved = models.BooleanField(default=False)
    privacy_blur = models.BooleanField(default=False) # Blur photos for non-premium/unconnected users
    last_activity = models.DateTimeField(null=True, blank=True)

    @property
    def completion_percentage(self):
        fields_to_check = [
            self.full_name, self.dob, self.gender, self.marital_status, self.height, self.photo,
            self.religion, self.caste, self.mother_tongue,
            self.highest_education, self.profession, self.annual_income,
            self.family_type, self.father_occupation, self.mother_occupation,
            self.city, self.state, self.country
        ]
        filled_fields = sum(1 for field in fields_to_check if field)
        return int((filled_fields / len(fields_to_check)) * 100)

    @property
    def age(self):
        from datetime import date
        if self.dob:
            today = date.today()
            return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return None
    
    # Step 2: Religion & Community
    religion = models.CharField(max_length=50, blank=True, null=True)
    caste = models.CharField(max_length=50, blank=True, null=True)
    mother_tongue = models.CharField(max_length=50, blank=True, null=True)
    
    # Step 3: Education & Career
    highest_education = models.CharField(max_length=100, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    annual_income = models.CharField(max_length=50, blank=True, null=True)
    
    # Step 4: Family Details
    family_type = models.CharField(max_length=50, blank=True, null=True)
    father_occupation = models.CharField(max_length=100, blank=True, null=True)
    mother_occupation = models.CharField(max_length=100, blank=True, null=True)
    siblings = models.IntegerField(default=0)
    
    # Step 5: Location Details
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    taluka = models.CharField(max_length=100, blank=True, null=True)
    village = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    # Step 6: Partner Preferences
    pref_age_min = models.IntegerField(blank=True, null=True)
    pref_age_max = models.IntegerField(blank=True, null=True)
    pref_religion = models.CharField(max_length=50, blank=True, null=True)
    
    # Step 5 (part 2): Bio
    about_me = models.TextField(blank=True, null=True)
    
    # Workflow Status
    APPROVAL_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES, default='Pending', db_index=True)
    
    PAYMENT_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    )
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='Pending', db_index=True)
    
    # 3-Tier Membership Plan Fields
    active_plan = models.ForeignKey('payments_app.MembershipPlan', null=True, blank=True, on_delete=models.SET_NULL, related_name='active_profiles')
    plan_expiry_date = models.DateTimeField(null=True, blank=True)
    interests_sent_count = models.IntegerField(default=0)
    is_banned = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Privacy Settings
    blur_profile_photo = models.BooleanField(default=False)
    hide_contact_info = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=True)
    sms_alerts = models.BooleanField(default=False)


    @property
    def is_online(self):
        from django.utils import timezone
        if self.last_activity:
            now = timezone.now()
            diff = now - self.last_activity
            return diff.total_seconds() < 300
        return False


    @property
    def is_verified(self):
        try:
            return self.user.kyc.status == 'Approved'
        except Exception:
            return False

    def __str__(self):
        return f"{self.user.username}'s Profile"


class ProfileGallery(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='gallery_photos')
    photo = models.ImageField(upload_to='gallery_photos/')
    is_approved = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Religion(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name

class Caste(models.Model):
    religion = models.ForeignKey(Religion, on_delete=models.CASCADE, related_name='castes')
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    def __str__(self): return f"{self.name} ({self.religion.name})"
    class Meta:
        unique_together = ('religion', 'name')

class MotherTongue(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name

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
