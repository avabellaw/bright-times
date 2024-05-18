from django.shortcuts import render, redirect
from .models import Ticket
from events.models import Event
from django.contrib import messages
from django.conf import settings
from templates.includes.decorators import login_required_message

ToastMessage = settings.TOAST_MESSAGE


@login_required_message
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
        for _ in range(quantity):
            ticket = Ticket.objects.create(event=event, user=request.user)
            ticket.save()

        MESSAGE = f'Ticket for "{event.name}" purchased successfully.'

        messages.success(request, MESSAGE)

        return redirect('events')

    template = 'events/tickets/buy-ticket.html'

    context = {
        'event': event,
    }

    return render(request, template, context)
