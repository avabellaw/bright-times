import os

from dateutil import parser

from datetime import datetime

from .models import Event


def get_available_events():
    """Return a list of events that have tickets available"""
    today = get_todays_date()

    avail_event_ids = [event.id
                       for event in Event.objects.exclude(
                           ticket_end_date_time__lt=today)
                       if event.get_tickets_left() > 0]

    return Event.objects.filter(id__in=avail_event_ids)


def get_todays_date():
    DEMO_DATE = os.environ.get('DEMO_DATE', '')
    if DEMO_DATE:
        return parser.parse(DEMO_DATE)
    else:
        return datetime.today()
