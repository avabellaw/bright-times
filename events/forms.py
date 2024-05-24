from django import forms
from .models import Venue, Address, Event


class FormUtilsMixin():
    def make_read_only(self):
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True
            field.widget.attrs['disabled'] = True


class EventForm(forms.ModelForm, FormUtilsMixin):
    class Meta():
        model = Event
        exclude = ['venue', 'created_by_venue_manager']

        datetime_attributes = {'type': 'datetime-local',
                               'class': 'datetimepicker'}

        widgets = {
            'start_date_time': forms.DateTimeInput(attrs=datetime_attributes),
            'end_date_time': forms.DateTimeInput(attrs=datetime_attributes),
            'ticket_end_date_time': forms.DateTimeInput(
                attrs=datetime_attributes),
        }


class VenueForm(forms.ModelForm, FormUtilsMixin):
    class Meta():
        model = Venue
        exclude = ['address', 'managers']


class AddressForm(forms.ModelForm, FormUtilsMixin):
    class Meta():
        model = Address
        fields = "__all__"
