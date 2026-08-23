from django.shortcuts import render

def my_profile(request):
    return render(request, 'web/my_profile.html')

def saved_profiles(request):
    return render(request, 'web/saved_profiles.html')

def verified_profiles(request):
    return render(request, 'web/verified_profiles.html')

def basic_search(request):
    return render(request, 'web/basic_search.html')

def advanced_search(request):
    return render(request, 'web/advanced_search.html')

def ai_search(request):
    return render(request, 'web/ai_search.html')

def saved_searches(request):
    return render(request, 'web/saved_searches.html')

def matches1(request):
    return render(request, 'web/matches1.html')

def matches2(request):
    return render(request, 'web/matches2.html')

def nearby_match(request):
    return render(request, 'web/nearby-match.html')

def recomended_matches(request):
    return render(request, 'web/recomended-matches.html')

def todays_matches(request):
    return render(request, 'web/todays-matches.html')

def Ai_match(request):
    return render(request, 'web/Ai-match.html')

def featured_brides(request):
    return render(request, 'web/featured_brides.html')

def featured_grooms(request):
    return render(request, 'web/featured_grooms.html')

def personal(request):
    return render(request, 'web/personal.html')

