from events.models import VenueManager, Event


def user_context(request):
    user = request.user
    if user.is_authenticated:
        manager_objects = VenueManager.objects.filter(user=user)
        user.is_venue_manager = True if len(manager_objects) > 0 else False

        user_events = Event.objects.filter(managers=user)
        user.has_events = True if len(user_events) > 0 else False

        return {
            'user': user,
        }
    return {}
