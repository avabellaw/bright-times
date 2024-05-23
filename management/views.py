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

    venue_form = VenueForm(instance=venue)
    venue_form.make_read_only()
    address_form = AddressForm(instance=venue.address)
    address_form.make_read_only()

    template = 'management/venue/venue-detail.html'

    context = {
        'venue': venue,
        'venue_form': venue_form,
        'address_form': address_form,
    }

    return render(request, template, context)
