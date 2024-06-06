from events.models import VenueManager, Event
from user_profile.models import UserProfile
from tickets.models import Ticket


def user_context(request):
    user = request.user
    if user.is_authenticated:
        manager_objects = VenueManager.objects.filter(user=user)
        user.is_venue_manager = len(manager_objects) > 0
        user.is_venue_admin = False
        user.is_venue_owner = False

        for obj in manager_objects:
            if obj.role == 'OWNER':
                user.is_venue_owner = True
                user.is_venue_admin = True
                break
            if obj.role == 'MANAGER':
                user.is_venue_admin = True
                user.is_venue_owner = False
                break

        user_events = Event.objects.filter(venue__managers=user)
        user.has_events = len(user_events) > 0
        user.profile = UserProfile.objects.get(user=user)

        user.tickets = Ticket.objects.filter(user=user)

        return {
            'user': user,
        }
    return {}
