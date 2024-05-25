from events.models import VenueManager, Event
from user_profile.models import UserProfile


def user_context(request):
    user = request.user
    if user.is_authenticated:
        manager_objects = VenueManager.objects.filter(user=user)
        user.is_venue_manager = len(manager_objects) > 0
        user.is_venue_admin = False

        roles = [manager.role for manager in manager_objects]

        if "OWNER" in roles or "MANAGER" in roles:
            user.is_venue_admin = True

        user_events = Event.objects.filter(venue__managers=user)
        user.has_events = len(user_events) > 0
        user.profile = UserProfile.objects.get(user=user)

        return {
            'user': user,
        }
    return {}
