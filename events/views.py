from django.shortcuts import render, redirect
from .forms import AddressForm, VenueForm
from django.contrib.auth.decorators import login_required
from .models import Event, Venue, VenueManager
from django.contrib import messages


def events(request):

    events = Event.objects.all()

    template = 'events/events.html'

    context = {
        'events': events,
    }

    return render(request, template, context)


@login_required
def choose_or_create_venue(request):
    # Venues associated with the current user/venue manager
    venues = Venue.objects.filter(managers=request.user)

    address_form = AddressForm()
    venue_form = VenueForm()

    template = 'events/venues/choose-or-create-venue.html'

    context = {
        'venues': venues,
        'address_form': address_form,
        'venue_form': venue_form,
    }

    return render(request, template, context)


@login_required
def create_event(request):
    address_form = AddressForm()
    venue_form = VenueForm()

    # Temporary - use create venue template
    template = 'events/event-creation/first-stage.html'

    context = {
        'address_form': address_form,
        'venue_form': venue_form,
    }

    return render(request, template, context)
