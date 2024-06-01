from datetime import datetime

from tickets.models import Ticket
from .models import Event


def get_tickets_left_for_event(event):
    num_of_tickets_sold = Ticket.objects.filter(event=event).count()
    tickets_left = event.venue.capacity - num_of_tickets_sold
    return tickets_left


def add_tickets_left_to_events(events):
    for event in events:
        event.tickets_left = get_tickets_left_for_event(event)
    return events


def get_available_events():
    """Return a list of events that have tickets available"""
    today = datetime.today()

    avail_event_ids = [event.id
                       for event in Event.objects.exclude(
                           ticket_end_date_time__lt=today)
                       if get_tickets_left_for_event(event) > 0]

    return Event.objects.filter(id__in=avail_event_ids)
