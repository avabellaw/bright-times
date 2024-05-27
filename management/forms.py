from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from events.models import Venue, VenueManager


# Django docs for validation [https://docs.djangoproject.com/en/5.0/ref/forms/validation/]
# Django docs for select feilds [https://docs.djangoproject.com/en/5.0/ref/forms/fields/#choicefield]
class VenueManagerCreationForm(forms.Form):
    user = forms.CharField()
    venue = forms.ModelChoiceField(queryset=Venue.objects.none())
    role = forms.ChoiceField(choices=[(role, role) for role in settings.VENUE_MANAGER_ROLE])

    def __init__(self, venues, *args, **kwargs):
        self.venues = venues
        super().__init__(*args, **kwargs)
        self.fields['venue'].queryset = venues

    def clean_user(self):
        username_or_email = self.cleaned_data.get('user')

        try:
            user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                raise forms.ValidationError('User does not exist.')

        return user

    def clean(self):
        cleaned_data = super().clean()

        user = cleaned_data.get('user')
        venue = cleaned_data.get('venue')

        if user and venue:
            if VenueManager.objects.filter(venue=venue, user=user).exists():
                raise forms.ValidationError(
                    'Venue manager already exists.')

    def save(self):
        user = self.cleaned_data['user']
        venue = self.cleaned_data['venue']
        role = self.cleaned_data['role']

        venue_manager = VenueManager(user=user, venue=venue, role=role)
        venue_manager.save()

        return venue_manager