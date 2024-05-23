from events.models import VenueManager


def user_context(request):
    user = request.user
    if user.is_authenticated:
        manager_objects = VenueManager.objects.filter(user=user)
        user.is_venue_manager = True if len(manager_objects) > 0 else False

        return {
            'user': user,
        }
    return {}
