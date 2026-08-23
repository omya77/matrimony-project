import os

def add_decorator_to_file(filepath, target_functions, decorator):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    out_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this line is a function definition
        if line.startswith('def '):
            func_name = line.split('(')[0][4:].strip()
            if func_name in target_functions:
                # Need to insert decorator right before this function
                # But wait, there might be other decorators already like @login_required
                # Let's insert it before the first decorator if possible, or just before def if no decorators
                # Actually, in Django, it's safer to put it after @login_required or just before the `def`
                # Let's look backwards for other decorators to find the insertion point
                
                # Check if @enforce_payment is already there
                already_has = False
                j = len(out_lines) - 1
                while j >= 0 and (out_lines[j].startswith('@') or out_lines[j].strip() == ''):
                    if decorator in out_lines[j]:
                        already_has = True
                        break
                    j -= 1
                    
                if not already_has:
                    out_lines.append(f"{decorator}\n")
                    
        out_lines.append(line)
        i += 1
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(out_lines)


profiles_funcs = ['saved_profiles', 'verified_profiles']
add_decorator_to_file('profiles_app/views.py', profiles_funcs, '@enforce_payment')

interactions_funcs = [
    'chat', 'requests', 'basic_search', 'advanced_search', 'ai_search', 'saved_searches',
    'matches1', 'matches2', 'nearby_match', 'recomended_matches', 'todays_matches',
    'Ai_match', 'featured_brides', 'featured_grooms'
]

# Ensure enforce_payment is imported in interactions_app/views.py
with open('interactions_app/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'from profiles_app.views import enforce_payment' not in content:
    with open('interactions_app/views.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines.insert(0, "from profiles_app.views import enforce_payment\n")
    with open('interactions_app/views.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)

add_decorator_to_file('interactions_app/views.py', interactions_funcs, '@enforce_payment')
print("Successfully patched decorators!")
