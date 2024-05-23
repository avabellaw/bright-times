from events.models import VenueManager


def is_user_manager_of_venue(user, venue):
    """Check if the user is a manager of the venue"""
    try:
        VenueManager.objects.get(user=user, venue=venue)
        return True
    except VenueManager.DoesNotExist:
        return False
