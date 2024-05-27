from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages

from utils.decorators import (login_required_message,
                              must_be_venue_manager)
from .helpers import is_user_manager_of_venue
from events.models import Venue, Event, VenueManager
from events.forms import VenueForm, AddressForm, EventForm
from .forms import VenueManagerCreationForm

ToastMessage = settings.TOAST_MESSAGE


# Venue management views

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
        ToastMessage.deleted_successfully(request, venue.name)
        venue.delete()
    else:
        ToastMessage.cannot_delete_venue_not_manager(request)
    return redirect(reverse('venue-management'))


# Event management views

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

        if event_form.is_valid():
            event_form.save()
    else:
        event_form = EventForm(instance=event)

    event_form.make_read_only()
    template = 'management/event/event-detail.html'

    context = {
        'event': event,
        'event_form': event_form,
        'breadcrumbs': [{'name': event.name}]
    }

    return render(request, template, context)


@login_required_message
@must_be_venue_manager
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if is_user_manager_of_venue(request.user, event.venue):
        ToastMessage.deleted_successfully(request, event.name)
        event.delete()
    else:
        ToastMessage.cannot_delete_event_not_manager(request)
    return redirect(reverse('event-management'))

# Venue manager admin views


@login_required_message
@must_be_venue_manager
def venue_manager_admin(request):
    template = 'management/venue-manager/venue-manager-admin.html'

    venues = Venue.objects.filter(
        venuemanager__user=request.user, venuemanager__role__in=['OWNER', 'MANAGER'])

    venue_managers = VenueManager.objects.filter(venue__in=venues).exclude(user=request.user)

    form = VenueManagerCreationForm(venues)

    if len(venues) == 0:
        ToastMessage.must_be_a_venue_manager(request)
        return redirect('create-or-choose-venue')

    if request.POST:
        form = VenueManagerCreationForm(venues, request.POST)

        if form.is_valid():
            form.save()
            user = form.cleaned_data['user']
            messages.success(request, f'Venue manager {user.username} added \
                successfully.')
            return redirect('venue-manager-admin')
        else:
            messages.error(request, 'Please correct the form errors.')

    context = {
        'venue_managers': venue_managers,
        'form': form,
    }

    return render(request, template, context)
