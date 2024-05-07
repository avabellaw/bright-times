from django.shortcuts import render, redirect
from .forms import AddressForm, VenueForm
from django.contrib.auth.decorators import login_required
from .models import Event
from django.contrib import messages


def events(request):

    events = Event.objects.all()

    template = 'events/events.html'

    context = {
        'events': events,
    }

    return render(request, template, context)


def create_event(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to create an event')
        return redirect('account_login')
    address_form = AddressForm()
    venue_form = VenueForm()

    # Temporary - use create venue template
    template = 'events/create_venue.html'

    context = {
        'address_form': address_form,
        'venue_form': venue_form,
    }

    return render(request, template, context)
