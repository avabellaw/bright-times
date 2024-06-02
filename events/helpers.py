from datetime import datetime

from tickets.models import Ticket
from .models import Event

def get_available_events():
    """Return a list of events that have tickets available"""
    today = datetime.today()

    avail_event_ids = [event.id
                       for event in Event.objects.exclude(
                           ticket_end_date_time__lt=today)
                       if event.get_tickets_left() > 0]

    return Event.objects.filter(id__in=avail_event_ids)
