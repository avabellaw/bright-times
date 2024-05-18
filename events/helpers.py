from tickets.models import Ticket


def get_tickets_left_for_event(event):
    num_of_tickets_sold = Ticket.objects.filter(event=event).count()
    tickets_left = event.venue.capacity - num_of_tickets_sold
    return tickets_left


def add_tickets_left_to_events(events):
    for event in events:
        event.tickets_left = get_tickets_left_for_event(event)
    return events
