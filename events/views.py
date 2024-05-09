from django.shortcuts import render, redirect
from .forms import AddressForm, VenueForm, EventForm
from django.contrib.auth.decorators import login_required
from .models import Event, Venue, VenueManager
from django.contrib import messages
from django.core.exceptions import PermissionDenied


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

    # Only new venue form information will be posted
    # Venue ID will be posted to create_event view
    if request.POST:
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
def create_event(request, venue_id=None):
    if venue_id is None:
        venue_id = int(request.POST.get('choose-venue'))

    venue = Venue.objects.get(id=venue_id)

    try:
        VenueManager.objects.get(venue=venue, user=request.user)
    except VenueManager.DoesNotExist:
        messages.error(request, "You're not a manager of this venue.")
        raise PermissionDenied

    event_form = EventForm()

    template = 'events/create_event.html'

    context = {
        'venue': venue,
        'event_form': event_form,
    }

    return render(request, template, context)
