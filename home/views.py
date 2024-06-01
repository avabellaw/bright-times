from django.shortcuts import render
from events.models import Event
from datetime import datetime, timedelta


def home(request):
    """View for homepage"""
    
    today = datetime.today()

    by_next_week = today + timedelta(weeks=1)
    coming_up = Event.objects.filter(
        start_date_time__lt=by_next_week
        ).exclude(ticket_end_date_time__lt=today).order_by('start_date_time')

    context = {
        'coming_up': coming_up
    }
    return render(request, 'home/index.html', context)
