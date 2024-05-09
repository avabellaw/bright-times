from django import forms
from .models import Venue, Address


class VenueForm(forms.ModelForm):
    class Meta():
        model = Venue
        exclude = ['address', 'managers']


class AddressForm(forms.ModelForm):
    class Meta():
        model = Address
        fields = "__all__"
