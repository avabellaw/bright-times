from django.shortcuts import render, redirect
from .models import Ticket
from events.models import Event
from django.conf import settings
from utils.decorators import login_required_message
import stripe
from decimal import Decimal
from django.http import JsonResponse
from django.urls import reverse
from utils.decorators import email_verification_required

ToastMessage = settings.TOAST_MESSAGE


@login_required_message
@email_verification_required
def buy_ticket(request, event_id):
    event = Event.objects.get(id=event_id)

    if request.POST:
        quantity = int(request.POST.get('quantity'))

        tickets_owned = Ticket.objects.filter(event=event,
                                              user=request.user).count()

        # Check if user has reached max tickets
        if tickets_owned + quantity > settings.MAX_TICKETS_PER_USER:
            ToastMessage.user_reached_max_tickets(request)
            return redirect('buy-ticket', event_id=event_id)

        # Check if quantity is valid
        if quantity < 1 or quantity > settings.MAX_TICKETS_PER_USER:
            ToastMessage.min_max_tickets_error(request, quantity)
            return redirect('buy-ticket', event_id=event_id)

        # Purchase tickets at quantity selected
        # for _ in range(quantity):
        #     ticket = Ticket.objects.create(event=event, user=request.user)
        #     ticket.save()

        # create_stripe_payment(request, event, quantity)

        # MESSAGE = f'Ticket for "{event.name}" purchased successfully.'

        # messages.success(request, MESSAGE)

        request.session['ticket_order'] = {
            'total': str(event.price * quantity)
        }
        return redirect('checkout', event_id=event_id)

    template = 'tickets/buy-ticket.html'

    context = {
        'event': event,
        'breadcrumbs': [
            {
                'name': event.name,
                'url': reverse('event-details', args=[event.id])
            },
            {
                'name': 'Buy ticket',
                'url': reverse('buy-ticket', args=[event.id])
            }
        ]
    }

    return render(request, template, context)


def checkout(request, event_id):
    stripe_pub_key = settings.STRIPE_PUBLISHABLE_KEY

    context = {
        'stripe_pub_key': stripe_pub_key,
        'event_id': event_id,
    }

    template = 'tickets/checkout.html'

    return render(request, template, context)


def create_payment_intent(request):
    ticket_order = request.session.get('ticket_order')
    order_total = Decimal(ticket_order.get('total'))
    print("order total: ", order_total)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=int(order_total * 100),
            currency='GBP',
        )
        return JsonResponse({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        print("ERROR:", e)
        return JsonResponse(error=str(e)), 403
