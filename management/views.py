from django.shortcuts import render
from templates.includes.decorators import (login_required_message,
                                           must_be_venue_manager)

from events.models import Venue


@login_required_message
@must_be_venue_manager
def venue_management(request):
    venues = Venue.objects.filter(managers=request.user)

    template = 'management/venue-management.html'

    context = {
        'venues': venues,
    }

    return render(request, template, context)
