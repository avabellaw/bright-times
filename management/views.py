from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages

from utils.decorators import (login_required_message,
                              must_be_venue_manager)
from .helpers import is_user_manager_of_venue, get_venues_managed_by_user
from events.models import Venue, Event, VenueManager
from events.forms import VenueForm, AddressForm, EventForm
from .forms import VenueManagerCreationForm
from .templatetags import management

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
            ToastMessage.updated_successfully(request, venue.name)
    else:
        venue_form = VenueForm(instance=venue)
        address_form = AddressForm(instance=venue.address)

    venue_form.make_read_only()
    address_form.make_read_only()
    venue_form.add_class_to_all_fields('editable-field')
    address_form.add_class_to_all_fields('editable-field')

    delete_url = reverse('delete-venue', args=[venue_id])

    template = 'management/venue/venue-detail.html'

    context = {
        'venue': venue,
        'venue_form': venue_form,
        'address_form': address_form,
        'breadcrumbs': [{'name': venue.name}],
        'delete_url': delete_url,
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
            ToastMessage.updated_successfully(request, event.name)
    else:
        event_form = EventForm(instance=event)

    event_form.make_read_only()
    event_form.add_class_to_all_fields('editable-field')

    delete_url = reverse('delete-event', args=[event_id])

    template = 'management/event/event-detail.html'

    context = {
        'event': event,
        'event_form': event_form,
        'breadcrumbs': [{'name': event.name}],
        'delete_url': delete_url,
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

    venues = get_venues_managed_by_user(request.user)

    venue_managers = VenueManager.objects.filter(
        venue__in=venues).exclude(user=request.user)

    form = VenueManagerCreationForm(venues)

    if len(venues) == 0:
        ToastMessage.must_be_a_venue_manager(request)
        return redirect('create-or-choose-venue')

    if request.POST:
        form = VenueManagerCreationForm(venues, request.POST)

        if form.is_valid():
            venue = form.cleaned_data['venue']
            user_role = management.manager_role(venue, request.user)

            if request.POST['role'] == 'OWNER' and not user_role == "OWNER":
                messages.error(request, 'Only owner can create a new owners.')
                return redirect('venue-manager-admin')
            form.save()
            messages.success(request, f'{form.venue_manager} added \
                successfully.')
            return redirect('venue-manager-admin')
        else:
            messages.error(request, 'Please correct the form errors.')

    context = {
        'venue_managers': venue_managers,
        'form': form,
    }

    return render(request, template, context)


@login_required_message
@must_be_venue_manager
def venue_manager_admin_detail(request, manager_id):
    manager = VenueManager.objects.get(pk=manager_id)

    if request.POST:
        role = request.POST.get('role')
        if role not in settings.VENUE_MANAGER_ROLE:
            messages.error(request, 'Invalid role.')
            return redirect(reverse('venue-manager-admin-detail',
                                    args=[manager_id]))

        manager.role = role
        manager.save()
        messages.success(request, 'Role updated successfully.')

    delete_url = reverse('delete-manager', args=[manager_id])

    template = 'management/venue-manager/venue-manager-detail.html'

    context = {
        'roles': settings.VENUE_MANAGER_ROLE,
        'manager': manager,
        'delete_url': delete_url,
    }

    return render(request, template, context)


@login_required_message
@must_be_venue_manager
def delete_manager(request, manager_id):
    manager = VenueManager.objects.get(pk=manager_id)
    if is_user_manager_of_venue(request.user, manager.venue):
        ToastMessage.deleted_successfully(request, manager)
        manager.delete()
    else:
        ToastMessage.cannot_delete_manager_not_manager(request)
    return redirect(reverse('venue-manager-admin'))
