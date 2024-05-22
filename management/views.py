from django.shortcuts import render


def venue_management(request):
    return render(request, 'management/venue-management.html')
