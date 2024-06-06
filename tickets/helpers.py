from events.models import Event
from decimal import Decimal


def get_ticket_order(request):
    """returns the ticket order from the session as an object"""
    ticket_order = request.session.get('ticket_order')

    event_id = ticket_order.get('item_id')
    event = Event.objects.get(id=event_id)
    qty = int(ticket_order.get('qty'))
    total = Decimal(event.price * qty)
    first_name = ticket_order.get('first_name')
    last_name = ticket_order.get('last_name')
    email = ticket_order.get('email')

    return TicketOrder(event, qty, total, first_name, last_name, email)


class TicketOrder():
    def __init__(self, event, qty, total, first_name, last_name, email):
        self.event = event
        self.qty = qty
        self.total = total
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def validate_payment_intent(self, payment_intent):
        """Return does the payment intent match the ticket order session"""
        is_amount_correct = payment_intent['amount'] == int(self.total * 100)
        is_currency_correct = payment_intent['currency'] == 'gbp'
        return is_amount_correct and is_currency_correct
