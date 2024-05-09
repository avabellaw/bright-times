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
def choose_or_create_venue(request, create_venue=False):
    # Venues associated with the current user/venue manager
    venues = Venue.objects.filter(managers=request.user)

    if request.POST:
        if create_venue:
            venue_form = VenueForm(request.POST)
            address_form = AddressForm(request.POST)

            if venue_form.is_valid() and address_form.is_valid():
                address = address_form.save()
                venue = venue_form.save(commit=False)
                venue.address = address
                venue.save(created_by=request.user)

                MESSAGE = f'Venue "{venue.name}" created successfully.'

                messages.success(request, MESSAGE)

                return redirect('create_event', venue_id=venue.id)
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
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
def create_event(request, venue_id):
    venue = Venue.objects.get(id=venue_id)

    template = 'events/create_event.html'

    context = {
        'venue': venue,
    }

    return render(request, template, context)
