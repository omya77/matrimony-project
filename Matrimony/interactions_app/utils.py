def calculate_match_score(user_profile, target_profile):
    """
    Calculates a Match Score (0-100%) between two profiles.
    Criteria (Total 100 points):
    1. Religion (Strict) - 30 points
    2. Caste (Strict) - 20 points
    3. Mother Tongue - 15 points
    4. Education (Basic Match) - 10 points
    5. Diet (Basic Match) - 10 points
    6. State/City (Proximity) - 15 points
    """
    if not user_profile or not target_profile:
        return 0

    score = 0
    
    # Safely get attributes using getattr to prevent crashes
    u_rel = getattr(user_profile, 'religion', None)
    t_rel = getattr(target_profile, 'religion', None)
    u_caste = getattr(user_profile, 'caste', None)
    t_caste = getattr(target_profile, 'caste', None)
    u_mt = getattr(user_profile, 'mother_tongue', None)
    t_mt = getattr(target_profile, 'mother_tongue', None)
    u_edu = getattr(user_profile, 'highest_education', None)
    t_edu = getattr(target_profile, 'highest_education', None)
    u_diet = getattr(user_profile, 'diet', None)
    t_diet = getattr(target_profile, 'diet', None)
    u_state = getattr(user_profile, 'state', None)
    t_state = getattr(target_profile, 'state', None)
    u_city = getattr(user_profile, 'city', None)
    t_city = getattr(target_profile, 'city', None)
    
    # 1. Religion (30)
    if u_rel and t_rel and u_rel == t_rel:
        score += 30
        
    # 2. Caste (20)
    if u_caste and t_caste and u_caste == t_caste:
        score += 20
        
    # 3. Mother Tongue (15)
    if u_mt and t_mt and u_mt == t_mt:
        score += 15
        
    # 4. Education (10)
    if u_edu and t_edu:
        if u_edu == t_edu:
            score += 10
        else:
            # Partial score if both are educated but different degrees
            score += 5
            
    # 5. Diet (10)
    if u_diet and t_diet and u_diet == t_diet:
        score += 10
        
    # 6. Location (15)
    if u_state and t_state and u_state == t_state:
        score += 10
        if u_city and t_city and u_city == t_city:
            score += 5 # Additional 5 for same city

    if score < 50 and u_rel and t_rel and u_rel == t_rel:
        score += 10
        
    # Cap at 100
    return min(score, 100)

