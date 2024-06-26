from django.shortcuts import render, redirect
from .forms import AddressForm, VenueForm, EventForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.urls import reverse

from utils.decorators import login_required_message
from .models import Event, Venue, VenueManager

ToastMessage = settings.TOAST_MESSAGE


def events(request):

    events = Event.objects.all()

    template = 'events/events.html'

    context = {
        'events': events,
    }

    return render(request, template, context)


def event_details(request, event_id):
    event = Event.objects.get(id=event_id)

    template = 'events/event-details.html'

    context = {
        'event': event,
        'breadcrumbs': [{'name': event.name, 'url': reverse('event-details',
                                                            args=[event.id])}],
    }

    return render(request, template, context)


@login_required_message
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

            return redirect('create-event', venue_id=venue.id)
        else:
            ToastMessage.form_validation_error(request)
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


@login_required_message
def select_venue(request):
    venue_id = int(request.POST.get('choose-venue'))
    return redirect('create-event', venue_id=venue_id)


@login_required_message
def create_event(request, venue_id):
    venue = Venue.objects.get(id=venue_id)

    try:
        VenueManager.objects.get(venue=venue, user=request.user)
    except VenueManager.DoesNotExist:
        ToastMessage.not_a_manager(request)
        raise PermissionDenied

    if request.POST:
        event_form = EventForm(request.POST, request.FILES)

        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.venue = venue
            event.save(created_by=request.user)

            MESSAGE = f'Event "{event.name}" created successfully.'

            messages.success(request, MESSAGE)

            return redirect('event-details', event_id=event.id)
        else:
            ToastMessage.form_validation_error(request)
    else:
        event_form = EventForm()

    template = 'events/create-event.html'

    context = {
        'venue': venue,
        'event_form': event_form,
    }

    return render(request, template, context)
