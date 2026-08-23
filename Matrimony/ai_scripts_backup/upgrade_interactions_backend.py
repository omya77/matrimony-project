import os
import re

with open('interactions_app/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update requests view
requests_view_new = """@login_required(login_url='/accounts/login/')
def requests(request):
    # Fetch received requests that are pending
    pending_received = InterestRequest.objects.filter(receiver=request.user, status='pending').select_related('sender__profile')

    # Fetch sent requests that are pending
    pending_sent = InterestRequest.objects.filter(sender=request.user, status='pending').select_related('receiver__profile')

    # Fetch accepted connections (where user is either sender or receiver)
    connections = InterestRequest.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        status='accepted'
    ).select_related('sender__profile', 'receiver__profile')

    context = {
        'pending_received': pending_received,
        'pending_sent': pending_sent,
        'connections': connections
    }
    return render(request, 'web/requests.html', context)
"""
content = re.sub(
    r'@login_required\(login_url=\'/accounts/login/\'\)\ndef requests\(request\):[\s\S]*?return render\(request, \'web/requests.html\', .*?\)',
    requests_view_new.strip(),
    content
)

# 2. Update AI search
ai_search_new = """def ai_search(request):
    matches = get_opposite_gender_profiles(request)
    query = request.GET.get('q', '')
    if query:
        matches = matches.filter(
            Q(bio__icontains=query) |
            Q(profession__icontains=query) |
            Q(city__icontains=query) |
            Q(highest_education__icontains=query)
        )
    return render(request, 'web/ai_search.html', {'matches': matches, 'query': query})
"""
content = re.sub(
    r'def ai_search\(request\):[\s\S]*?return render\(request, \'web/ai_search.html\', \{.*?\}\)',
    ai_search_new.strip(),
    content
)

# 3. Update Advanced search to be strict
advanced_search_new = """def advanced_search(request):
    matches = get_opposite_gender_profiles(request)
    if request.method == 'GET' and request.GET:
        # Religion & Caste
        religion = request.GET.get('religion')
        caste = request.GET.get('caste')
        if religion and religion != 'Select Religion':
            matches = matches.filter(religion__iexact=religion)
        if caste and caste != 'Select Caste / Sub-Caste' and caste != 'Any':
            matches = matches.filter(caste__iexact=caste)

        # Education & Profession
        education = request.GET.get('highest_education')
        profession = request.GET.get('profession')
        if education and education != 'Select Education':
            matches = matches.filter(highest_education__iexact=education)
        if profession and profession != 'Select Occupation':
            matches = matches.filter(profession__iexact=profession)

        # Location
        state = request.GET.get('state')
        city = request.GET.get('city')
        if state and state != 'Select State':
            matches = matches.filter(state__iexact=state)
        if city and city != 'Select City':
            matches = matches.filter(city__iexact=city)

    context = {'matches': matches, 'user_gender': request.session.get('user_gender', '')}
    return render(request, 'web/advanced_search.html', context)
"""
content = re.sub(
    r'def advanced_search\(request\):[\s\S]*?return render\(request, \'web/advanced_search.html\', context\)',
    advanced_search_new.strip(),
    content
)

# 4. Update recomended_matches logic
recomended_matches_new = """def recomended_matches(request):
    matches = get_opposite_gender_profiles(request)
    scored_matches = []

    try:
        user_profile = request.user.profile

        for match in matches:
            score = 50 # Base score for being opposite gender and approved

            # Religion Match (+30)
            if user_profile.pref_religion and user_profile.pref_religion != 'Any':
                if match.religion == user_profile.pref_religion:
                    score += 30

            # Mother Tongue Match (+10)
            if user_profile.mother_tongue and match.mother_tongue == user_profile.mother_tongue:
                score += 10

            # Location Match (+10)
            if user_profile.state and match.state == user_profile.state:
                score += 10

            # Cap at 100%
            score = min(score, 100)
            match.match_score = score
            scored_matches.append(match)

        # Sort by score descending
        scored_matches.sort(key=lambda x: x.match_score, reverse=True)

    except Exception as e:
        print("Recommendation Error:", e)
        scored_matches = list(matches)
        for m in scored_matches:
            m.match_score = 50

    return render(request, 'web/recomended-matches.html', {'matches': scored_matches})
"""
content = re.sub(
    r'def recomended_matches\(request\):[\s\S]*?return render\(request, \'web/recomended-matches.html\', \{.*?\}\)',
    recomended_matches_new.strip(),
    content
)

with open('interactions_app/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("interactions_app/views.py successfully updated with Advanced Logic.")
