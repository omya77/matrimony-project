from django import template
from interactions_app.models import InterestRequest
from django.db.models import Q

register = template.Library()

@register.simple_tag
def get_interaction_status(user, target_user):
    if not user.is_authenticated or not target_user:
        return 'none'
        
    req = InterestRequest.objects.filter(
        (Q(sender=user, receiver=target_user) | Q(sender=target_user, receiver=user))
    ).first()
    
    if not req:
        return 'none'
    
    if req.status == 'accepted':
        return 'accepted'
    elif req.status == 'pending':
        if req.sender == user:
            return 'pending_sent'
        else:
            return 'pending_received'
    elif req.status == 'rejected':
        return 'rejected'
        
    return 'none'
