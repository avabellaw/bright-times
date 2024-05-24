from django.shortcuts import render
from templates.includes.decorators import (login_required_message,
                                           must_be_venue_manager)

from events.models import Venue, Event
from events.forms import VenueForm, AddressForm, EventForm
from django.urls import reverse
from django.shortcuts import redirect
from django.conf import settings
from .helpers import is_user_manager_of_venue

ToastMessage = settings.TOAST_MESSAGE


@login_required_message
@must_be_venue_manager
def venue_management(request):
    venues = Venue.objects.filter(managers=request.user)

    template = 'management/venue/venue-management.html'

    context = {
        'venues': venues,
    }

    return render(request, template, context)


@login_required_message
@must_be_venue_manager
def venue_detail(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)

    if request.POST:
        venue_form = VenueForm(request.POST, instance=venue)
        address_form = AddressForm(request.POST, instance=venue.address)

        if venue_form.is_valid() and address_form.is_valid():
            venue = venue_form.save(commit=False)
            address = address_form.save()
            venue.address = address
            venue.save()
    else:
        venue_form = VenueForm(instance=venue)
        address_form = AddressForm(instance=venue.address)

    venue_form.make_read_only()
    address_form.make_read_only()
    template = 'management/venue/venue-detail.html'

    context = {
        'venue': venue,
        'venue_form': venue_form,
        'address_form': address_form,
        'breadcrumbs': [{'name': venue.name}]
    }

    return render(request, template, context)


@login_required_message
@must_be_venue_manager
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    if is_user_manager_of_venue(request.user, venue):
        ToastMessage.venue_deleted(request, venue)
        venue.delete()
    else:
        ToastMessage.cannot_delete_venue_not_manager(request)
    return redirect(reverse('venue-management'))


@login_required_message
@must_be_venue_manager
def event_management(request):
    events = Event.objects.filter(venue__managers=request.user)

    template = 'management/event/event-management.html'

    context = {
        'events': events,
    }

    return render(request, template, context)


@login_required_message
@must_be_venue_manager
def event_detail(request, event_id):
    event = Event.objects.get(pk=event_id)

    if request.POST:
        event_form = EventForm(request.POST, instance=event)
        address_form = AddressForm(request.POST, instance=event.address)

        if event_form.is_valid() and address_form.is_valid():
            event = event_form.save(commit=False)
            address = address_form.save()
            event.address = address
            event.save()
    else:
        event_form = EventForm(instance=event)
        address_form = AddressForm(instance=event.address)

    event_form.make_read_only()
    address_form.make_read_only()
    template = 'management/event/event-detail.html'

    context = {
        'event': event,
        'event_form': event_form,
        'address_form': address_form,
        'breadcrumbs': [{'name': event.name}]
    }

    return render(request, template, context)