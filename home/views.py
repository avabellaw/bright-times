from django.shortcuts import render
from events.models import Event
from datetime import datetime, timedelta
from events import helpers as event_helpers


def home(request):
    """View for homepage"""

    today = datetime.today()

    by_next_week = today + timedelta(weeks=1)
    past_week = today - timedelta(weeks=1)
    available_events = event_helpers.get_available_events()

    coming_up = available_events.filter(
        start_date_time__lt=by_next_week
        ).order_by('start_date_time')

    recently_added = available_events.filter(
        created_on__gt=past_week).order_by('-created_on')

    context = {
        'coming_up': coming_up,
        'recently_added': recently_added,
    }
    return render(request, 'home/index.html', context)
