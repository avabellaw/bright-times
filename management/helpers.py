from events.models import VenueManager, Venue


def is_user_manager_of_venue(user, venue):
    """Check if the user is a manager of the venue"""
    try:
        VenueManager.objects.get(user=user, venue=venue)
        return True
    except VenueManager.DoesNotExist:
        return False


def get_venues_managed_by_user(user):
    """Get venues managed by the user"""
    return Venue.objects.filter(
        venuemanager__user=user, venuemanager__role__in=['OWNER', 'MANAGER'])
