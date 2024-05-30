from django.shortcuts import render, redirect
from events.models import Event
from django.conf import settings
from utils.decorators import login_required_message
import stripe
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages

from utils.decorators import email_verification_required
from django.http import HttpResponseRedirect

from .helpers import get_ticket_order
from .models import Ticket, TicketOrder
from user_profile.models import UserProfile
import json

ToastMessage = settings.TOAST_MESSAGE


@login_required_message
def user_tickets(request):
    tickets = Ticket.objects.filter(user=request.user)

    template = 'tickets/user-tickets.html'

    context = {
        'tickets': tickets,
        'breadcrumbs': [
            {
                'name': 'My tickets',
                'url': reverse('user-tickets')
            }
        ]
    }

    return render(request, template, context)

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

        request.session['ticket_order'] = {
            'item_id': str(event.id),
            'qty': str(quantity),
            'total': str(event.price * quantity)
        }
        return redirect('checkout')

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


def create_order(request):
    payment_intent = request.GET.get('payment_intent')

    stripe.api_key = settings.STRIPE_SECRET_KEY

    confirmed_payment_intent = stripe.PaymentIntent.retrieve(
        str(payment_intent))

    payment_intent_object = json.loads(str(confirmed_payment_intent))

    ticket_order = get_ticket_order(request)
    is_valid = ticket_order.validate_payment_intent(payment_intent_object)

    if is_valid:
        ticket_order = get_ticket_order(request)
        event = ticket_order.event
        qty = ticket_order.qty

        customer = stripe.Customer.retrieve(payment_intent_object["customer"])
        email = customer.email
        order = TicketOrder.objects.filter(
            payment_intent=confirmed_payment_intent)
        if order.exists():
            order = order.first()
            messages.error(request, 'Order already exists.')
        else:
            # Create the order
            order = TicketOrder.objects.create(
                first_name="TEMP FIRST",
                last_name="TEMP LAST",
                email=email,
                quantity=qty,
                price=event.price,
                order_total=ticket_order.total,
                payment_intent=confirmed_payment_intent
            )

            # Create the tickets
            for _ in range(qty):
                ticket = Ticket.objects.create(event=event, user=request.user,
                                               order_num=order)
                ticket.save()

            del request.session['ticket_order']

            MESSAGE = f'{qty} x ticket(s) for "{
                event.name}" purchased successfully.'

            messages.success(request, MESSAGE)

        return HttpResponseRedirect(reverse('checkout-success',
                                            args=[order.order_num]))


def checkout(request):
    ticket_order = get_ticket_order(request)

    event = ticket_order.event
    qty = ticket_order.qty
    event_id = ticket_order.event.id
    total = ticket_order.total

    stripe_pub_key = settings.STRIPE_PUBLISHABLE_KEY
    template = 'tickets/checkout.html'

    context = {
        'event': event,
        'qty': qty,
        'total': total,
        'stripe_pub_key': stripe_pub_key,
        'event_id': event_id,
    }

    return render(request, template, context)


def checkout_success(request, order_num):
    order = TicketOrder.objects.get(order_num=order_num)
    a_ticket = Ticket.objects.filter(order_num=order.order_num).first()
    event = Event.objects.get(id=a_ticket.event.id)

    template = 'tickets/checkout-success.html'

    context = {
        'order': order,
        'event': event,
    }

    return render(request, template, context)


def create_payment_intent(request):
    ticket_order = get_ticket_order(request)
    order_total = ticket_order.total
    user_profile = UserProfile.objects.get(user=request.user)

    desc = f'{ticket_order.qty} x ticket(s) for {ticket_order.event.name}.\n\n\
        Ticket price: £{ticket_order.event.price}.\n\
        Total: £{order_total}.'
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        # Create a PaymentIntent with the order amount and currency
        # Stripe docs [https://docs.stripe.com/api/payment_intents/create]
        if user_profile.stripe_customer_id:
            customer = stripe.Customer.retrieve(
                user_profile.stripe_customer_id)
        else:
            customer = stripe.Customer.create(
                email=request.user.email,
                name=request.user.username,
            )

        intent = stripe.PaymentIntent.create(
            amount=int(order_total * 100),
            currency='gbp',
            customer=customer.id,
            description=desc
        )
        return JsonResponse({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        print("ERROR:", e)
        return JsonResponse(error=str(e)), 403
