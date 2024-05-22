from django.shortcuts import render
from templates.includes.decorators import (login_required_message,
                                           must_be_venue_manager)


@login_required_message
@must_be_venue_manager
def venue_management(request):

    return render(request, 'management/venue-management.html')
