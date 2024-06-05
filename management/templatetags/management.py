
from django.template import Library
from django.http import request
from events.models import VenueManager

register = Library()


@register.simple_tag
def manager_role(venue_id, user):
    try:
        venue_manager = VenueManager.objects.get(venue_id=venue_id,
                                                 user=user)
    except VenueManager.DoesNotExist:
        return None
    return venue_manager.role
