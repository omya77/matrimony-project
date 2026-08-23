from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from admin_panel.models import ContactMessage, SuccessStory, PlatformSetting
from django.contrib import messages

def index(request):
    try:
        heading = PlatformSetting.objects.get(key='website_heading').value
        description = PlatformSetting.objects.get(key='website_description').value
    except Exception:
        heading = "ForeverBond"
        description = "Where Beautiful Journeys Begin"
        
    context = {
        'website_heading': heading,
        'website_description': description
    }
    return render(request, 'web/index.html', context)

def Home(request):
    return render(request, 'web/Home.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            
            messages.success(request, "Your message has been sent successfully. We will get back to you soon!")
            return redirect('contact')
        else:
            messages.error(request, "Please fill in all required fields.")
            
    return render(request, 'web/contact.html')

def story_page(request):
    stories = SuccessStory.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'web/story_page.html', {'stories': stories})

def submit_story(request):
    if request.method == 'POST':
        couple_name = request.POST.get('couple_name')
        wedding_date = request.POST.get('wedding_date')
        story_text = request.POST.get('story_text')
        photo = request.FILES.get('photo')
        if couple_name and wedding_date and story_text:
            SuccessStory.objects.create(
                couple_name=couple_name,
                wedding_date=wedding_date,
                story_text=story_text,
                photo=photo
            )
            messages.success(request, 'Your success story has been submitted and is pending approval.')
        else:
            messages.error(request, 'Please provide all required details.')
    return redirect('story_page')

def Latest_article(request):
    return render(request, 'web/Latest-article.html')

def relationship_tips(request):
    return render(request, 'web/relationship_tips.html')

def marriage_advice(request):
    return render(request, 'web/marriage_advice.html')

def trust(request):
    return render(request, 'web/trust.html')

def Read_more(request):
    return render(request, 'web/Read-more.html')

def tips1(request):
    return render(request, 'web/tips1.html')


from django.http import JsonResponse
def submit_counseling_query(request):
    return JsonResponse({'status': 'success'})

