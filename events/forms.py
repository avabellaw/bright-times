from django import forms
from .models import Venue, Address, Event


class EventForm(forms.ModelForm):
    class Meta():
        model = Event
        exclude = ['venue', 'created_by_venue_manager']
        widgets = {
            'start_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'ticket_end_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class VenueForm(forms.ModelForm):
    class Meta():
        model = Venue
        exclude = ['address', 'managers']


class AddressForm(forms.ModelForm):
    class Meta():
        model = Address
        fields = "__all__"
