import os
import re

interactions_file = r"c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\interactions_app\views.py"
profiles_file = r"c:\Users\Omkar\Desktop\Matrimony_regis omkar\Matrimony_regis omkar\Matrimony\Matrimony\profiles_app\views.py"

helper_func = """
def attach_interest_status(request, profiles):
    if not request.user.is_authenticated:
        return profiles
    try:
        from interactions_app.models import InterestRequest
        sent_requests = dict(InterestRequest.objects.filter(sender=request.user).values_list('receiver_id', 'status'))
        received_requests = dict(InterestRequest.objects.filter(receiver=request.user, status='accepted').values_list('sender_id', 'status'))
        for profile in profiles:
            if profile.user.id in sent_requests:
                profile.interest_status = sent_requests[profile.user.id]
            elif profile.user.id in received_requests:
                profile.interest_status = 'accepted'
    except Exception as e:
        print("Error attaching interest status:", e)
    return profiles
"""

def process_file(filepath, is_interactions=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if "def attach_interest_status" not in content and is_interactions:
        content = helper_func + "\n" + content

    if not is_interactions and "attach_interest_status" not in content:
        content = "from interactions_app.views import attach_interest_status\n" + content

    # Find all render functions that pass matches
    # We will just inject attach_interest_status right before render
    
    # regex to find: return render(request, '...', {'matches': matches...})
    # We can replace: return render(request, template, context)
    # Actually, a simpler regex for views:
    
    views_to_patch = [
        "ai_search", "saved_searches", "matches1", "matches2",
        "nearby_match", "todays_matches", "Ai_match", "featured_brides", "featured_grooms",
        "saved_profiles", "verified_profiles"
    ]
    
    for view in views_to_patch:
        # We look for the definition of the view
        pattern = r"(def " + view + r"\(request\):.*?)(return render\()"
        
        def replacer(match):
            prefix = match.group(1)
            # if we have scored_matches, use that
            if "scored_matches" in prefix:
                prefix += "    scored_matches = attach_interest_status(request, scored_matches)\n    "
            elif "matches =" in prefix:
                prefix += "    matches = attach_interest_status(request, matches)\n    "
            return prefix + match.group(2)
            
        content = re.sub(pattern, replacer, content, flags=re.DOTALL)
        
    # special case for recomended_matches (has a try/except block)
    if "def recomended_matches" in content:
        pattern = r"(def recomended_matches\(request\):.*?)(return render\()"
        def replacer2(match):
            prefix = match.group(1)
            if "scored_matches =" in prefix and "attach_interest_status" not in prefix:
                prefix += "    scored_matches = attach_interest_status(request, scored_matches)\n    "
            return prefix + match.group(2)
        content = re.sub(pattern, replacer2, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")

process_file(interactions_file, True)
process_file(profiles_file, False)
