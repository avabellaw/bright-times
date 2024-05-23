from django.shortcuts import render
from templates.includes.decorators import (login_required_message,
                                           must_be_venue_manager)

from events.models import Venue
from events.forms import VenueForm, AddressForm


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
    }

    return render(request, template, context)
