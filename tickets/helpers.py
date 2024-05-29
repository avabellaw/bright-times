from events.models import Event
from decimal import Decimal


def get_ticket_order(request):
    ticket_order = request.session.get('ticket_order')

    event_id = ticket_order.get('item_id')
    event = Event.objects.get(id=event_id)
    qty = int(ticket_order.get('qty'))
    total = Decimal(event.price * qty)

    return TicketOrder(event, qty, total)


class TicketOrder():
    def __init__(self, event, qty, total):
        self.event = event
        self.qty = qty
        self.total = total
