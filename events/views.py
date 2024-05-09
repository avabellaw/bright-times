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


@login_required
def create_event(request):
    address_form = AddressForm()
    venue_form = VenueForm()

    # Temporary - use create venue template
    template = 'events/create_venue.html'

    context = {
        'address_form': address_form,
        'venue_form': venue_form,
    }

    return render(request, template, context)
