def website_settings(request):
    try:
        from admin_panel.models import PlatformSetting
        privacy = PlatformSetting.objects.get(key='privacy_policy_url').value
        terms = PlatformSetting.objects.get(key='terms_url').value
    except Exception:
        privacy = "javascript:void(0);"
        terms = "javascript:void(0);"
        
    return {
        'global_privacy_policy_url': privacy,
        'global_terms_url': terms
    }
