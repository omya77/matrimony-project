from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .models import Profile

from django.shortcuts import redirect

def enforce_payment(view_func):
    def _wrapped_view(request, *args, **kwargs):
        try:
            profile = request.user.profile
            if profile.payment_status != 'Paid':
                return redirect('/payments/checkout/')
        except:
            pass
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required(login_url='/accounts/login/')
# =====================
# User ?? Personal Details Save ???
# =====================
def personal(request):
    if request.method == 'POST':
        try:
            profile, created = Profile.objects.get_or_create(user=request.user)
            
            if request.content_type == 'application/json':
                import json
                data = json.loads(request.body)
            else:
                data = request.POST

            # Backend Validation
            required_fields = {
                'userName': 'Full Name',
                'userDob': 'Date of Birth',
                'userGender': 'Gender',
                'maritalStatus': 'Marital Status',
                'userHeight': 'Height',
                'userReligion': 'Religion',
                'userCaste': 'Caste',
                'motherTongue': 'Mother Tongue',
                'highestEducation': 'Education',
                'profession': 'Profession',
                'city': 'City',
                'state': 'State'
            }
            
            missing_fields = []
            for key, label in required_fields.items():
                val = data.get(key)
                if not val or (isinstance(val, str) and not val.strip()) or (isinstance(val, str) and val.startswith('Select')):
                    missing_fields.append(label)
                    
            if missing_fields:
                return JsonResponse({
                    'status': 'error', 
                    'message': f"Please provide valid information for: {', '.join(missing_fields)}"
                }, status=400)
                
            # Age Validation
            dob_str = data.get('userDob')
            if dob_str:
                from datetime import datetime
                try:
                    dob = datetime.strptime(dob_str, "%Y-%m-%d")
                    today = datetime.today()
                    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                    if age < 21:
                        return JsonResponse({'status': 'error', 'message': 'Minimum age requirement is 21 years.'}, status=400)
                except Exception:
                    pass

            # Step 1
            profile.full_name = data.get('userName', profile.full_name)
            profile.dob = data.get('userDob', profile.dob)
            profile.gender = data.get('userGender', profile.gender)
            profile.marital_status = data.get('maritalStatus', profile.marital_status)
            profile.height = data.get('userHeight', profile.height)
            
            # Step 2
            profile.religion = data.get('userReligion', profile.religion)
            profile.caste = data.get('userCaste', profile.caste)
            profile.mother_tongue = data.get('motherTongue', profile.mother_tongue)
            
            # Step 3
            profile.highest_education = data.get('highestEducation', profile.highest_education)
            profile.profession = data.get('profession', profile.profession)
            profile.annual_income = data.get('annualIncome', profile.annual_income)
            
            # Step 4
            profile.family_type = data.get('familyType', profile.family_type)
            profile.father_occupation = data.get('fatherOccupation', profile.father_occupation)
            profile.mother_occupation = data.get('motherOccupation', profile.mother_occupation)
            profile.siblings = data.get('siblings', profile.siblings)
            
            # Step 5
            profile.city = data.get('city', profile.city)
            profile.state = data.get('state', profile.state)
            profile.country = data.get('country', profile.country)
            
            # Step 6
            profile.pref_age_min = data.get('prefAgeMin', profile.pref_age_min)
            profile.pref_age_max = data.get('prefAgeMax', profile.pref_age_max)
            profile.pref_religion = data.get('prefReligion', profile.pref_religion)
            
            # Step 5 (part 2): Bio
            profile.about_me = data.get('aboutMeDescription', profile.about_me)
            
            if 'photo' in request.FILES:
                profile.photo = request.FILES['photo']
                
                from admin_panel.models import PlatformSetting
                auto_approve = False
                try:
                    setting = PlatformSetting.objects.get(key='Auto-Approve Photos')
                    auto_approve = (setting.value == 'True')
                except Exception:
                    pass
                profile.is_photo_approved = auto_approve
            
            profile.save()
            if profile.payment_status == 'Paid':
                redirect_url = '/profiles/my-profile/'
            else:
                redirect_url = '/payments/checkout/'
            return JsonResponse({'status': 'success', 'message': 'Profile saved successfully!', 'redirect_url': redirect_url})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    # Render template on GET
    from .models import Religion, Caste, MotherTongue
    context = {
        'master_religions': Religion.objects.filter(is_active=True),
        'master_castes': Caste.objects.filter(is_active=True).select_related('religion'),
        'master_tongues': MotherTongue.objects.filter(is_active=True)
    }
    return render(request, 'web/personal.html', context)

@login_required(login_url='/accounts/login/')
def my_profile(request):
    profile = None
    try:
        profile = request.user.profile
    except Exception:
        pass
    return render(request, 'web/my_profile.html', {'profile': profile})

@login_required(login_url='/accounts/login/')
@enforce_payment
def saved_profiles(request):
    from interactions_app.models import SavedProfile
    from interactions_app.views import attach_interest_status
    from django.core.paginator import Paginator
    saved = SavedProfile.objects.filter(user=request.user).select_related('profile')
    matches = [s.profile for s in saved]
    for m in matches:
        m.is_saved = True
    matches = attach_interest_status(request, matches)
    
    paginator = Paginator(matches, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'web/saved_profiles.html', {'matches': page_obj})

@login_required(login_url='/accounts/login/')
@enforce_payment
def verified_profiles(request):
    from interactions_app.models import SavedProfile
    from interactions_app.views import get_opposite_gender_profiles, attach_interest_status
    matches = get_opposite_gender_profiles(request)
    matches = attach_interest_status(request, matches)
    if request.user.is_authenticated:
        saved_profile_ids = set(SavedProfile.objects.filter(user=request.user).values_list('profile_id', flat=True))
        for m in matches:
            m.is_saved = m.id in saved_profile_ids
    else:
        for m in matches:
            m.is_saved = False
    from django.core.paginator import Paginator
    paginator = Paginator(matches, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'web/verified_profiles.html', {'matches': page_obj})

from django.shortcuts import redirect
from django.contrib import messages

@login_required(login_url='/accounts/login/')
def upload_photo(request):
    if request.method == 'POST' and request.FILES.get('photo'):
        profile = getattr(request.user, 'profile', None)
        if profile:
            profile.photo = request.FILES['photo']
            
            from admin_panel.models import PlatformSetting
            auto_approve = False
            try:
                setting = PlatformSetting.objects.get(key='Auto-Approve Photos')
                auto_approve = (setting.value == 'True')
            except Exception:
                pass
            profile.is_photo_approved = auto_approve
            
            profile.save()
            messages.success(request, 'Photo uploaded successfully!')
        else:
            messages.error(request, 'Profile not found.')
    return redirect('/profiles/my-profile/')

from interactions_app.models import ProfileVisit

@login_required(login_url='/accounts/login/')
def who_viewed_me(request):
    profile = request.user.profile
    # Only premium users can see this
    if profile.payment_status != 'Paid':
        # Get count to show them what they are missing
        view_count = ProfileVisit.objects.filter(viewed_profile=profile).count()
        return render(request, 'web/who_viewed_me.html', {'is_premium': False, 'view_count': view_count})
    
    visits = ProfileVisit.objects.filter(viewed_profile=profile).select_related('viewer__profile').order_by('-timestamp')
    return render(request, 'web/who_viewed_me.html', {'is_premium': True, 'visits': visits})

from django.http import JsonResponse
import json

@login_required
def update_privacy(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        blur_profile_photo = data.get('privacy_blur', False)
        profile = request.user.profile
        profile.blur_profile_photo = blur_profile_photo
        profile.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

from django.shortcuts import redirect
from .models import ProfileGallery

@login_required
def upload_gallery(request):
    if request.method == 'POST':
        photo = request.FILES.get('gallery_photo')
        if photo:
            profile = request.user.profile
            if profile.gallery_photos.count() < 5:
                ProfileGallery.objects.create(profile=profile, photo=photo)
    return redirect('my_profile')

from .models import KYCDocument
from django.contrib import messages

@login_required
def upload_kyc(request):
    if request.method == 'POST':
        document_type = request.POST.get('document_type')
        document_file = request.FILES.get('document_file')
        if document_type and document_file:
            # Check if exists
            kyc, created = KYCDocument.objects.get_or_create(user=request.user)
            kyc.document_type = document_type
            kyc.document_file = document_file
            kyc.status = 'Pending'
            kyc.save()
            messages.success(request, 'KYC Document uploaded successfully and is pending review.')
    return redirect('my_profile')

