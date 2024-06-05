from django import forms
from .models import Venue, Address, Event
from django.forms.widgets import FileInput


class FormUtilsMixin():
    def make_read_only(self):
        for field in self.fields.values():
            if not (isinstance(field.widget, FileInput)
                    or isinstance(field.widget, forms.Select)):
                field.widget.attrs['readonly'] = True
            field.widget.attrs['disabled'] = True

    def add_class_to_all_fields(self, class_name):
        for field in self.fields.values():
            field.widget.attrs['class'] = class_name


class EventForm(forms.ModelForm, FormUtilsMixin):
    class Meta():
        model = Event
        fields = ['name', 'desc', 'about', 'price', 'image', 'start_date_time', 'end_date_time', 'ticket_end_date_time']

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

    def clean_postcode(self):
        postcode = self.cleaned_data['postcode']
        return postcode.upper()
