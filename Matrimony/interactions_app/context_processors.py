from interactions_app.models import InterestRequest, ChatMessage, Notification

def navbar_badges(request):
    """
    Context processor to inject unread requests count into all templates.
    """
    if request.user.is_authenticated:
        unread_requests_count = InterestRequest.objects.filter(receiver=request.user, status='pending', is_viewed=False).count()
        unread_messages_count = ChatMessage.objects.filter(receiver=request.user, is_read=False, deleted_by_receiver=False).count()
        unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
        
        return {
            'unread_requests_count': unread_requests_count,
            'unread_messages_count': unread_messages_count,
            'unread_notifications_count': unread_notifications_count,
            'notifications': notifications
        }
    return {
        'unread_requests_count': 0,
        'unread_messages_count': 0,
        'unread_notifications_count': 0,
        'notifications': []
    }

def master_data(request):
    try:
        from profiles_app.models import Religion, Caste, MotherTongue
        from payments_app.models import MembershipPlan
        return {
            'master_religions': Religion.objects.filter(is_active=True),
            'master_castes': Caste.objects.filter(is_active=True).select_related('religion'),
            'master_tongues': MotherTongue.objects.filter(is_active=True),
            'active_membership_plans': MembershipPlan.objects.filter(is_active=True).order_by('price')
        }
    except Exception:
        return {}
