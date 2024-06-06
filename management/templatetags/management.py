
from django.template import Library
from events.models import VenueManager

register = Library()


@register.simple_tag
def manager_role(venue_id, user):
    return get_manager_instance(venue_id, user).role


@register.simple_tag
def is_venue_admin(venue_id, user):
    role = manager_role(venue_id, user)

    return True if role == 'ADMIN' or role == 'OWNER' else False


@register.simple_tag
def get_manager_instance(venue_id, user):
    try:
        venue_manager = VenueManager.objects.get(venue_id=venue_id,
                                                 user=user)
    except VenueManager.DoesNotExist:
        return None
    return venue_manager
