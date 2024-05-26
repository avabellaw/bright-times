from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from events.models import Venue, VenueManager


# Django docs for validation [https://docs.djangoproject.com/en/5.0/ref/forms/validation/]
# Django docs for select feilds [https://docs.djangoproject.com/en/5.0/ref/forms/fields/#choicefield]
class VenueManagerCreationForm(forms.ModelForm):
    class Meta():
        model = VenueManager
        fields = ['user', 'venue', 'role']
        widgets = {
            'user': forms.TextInput(),
            'venue': forms.Select(),
            'role': forms.Select(choices=[(role, role)
                                          for role in settings.VENUE_MANAGER_ROLE]),
        }

    def __init__(self, venues, *args, **kwargs):
        super(VenueManagerCreationForm, self).__init__(*args, **kwargs)
        venues = [(venue.id, venue.name) for venue in venues]
        self.fields['venue'].choices = venues

    def clean_user(self):
        username_or_email = self.cleaned_data['user']

        try:
            user = User.objects.get(username=username_or_email)
            return user
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username_or_email)
                return user
            except User.DoesNotExist:
                raise forms.ValidationError('User does not exist.')

    def clean_venue(self):
        venue_id = self.cleaned_data['venue']

        try:
            venue = Venue.objects.get(pk=venue_id)
            return venue
        except Venue.DoesNotExist:
            raise forms.ValidationError('Venue does not exist.')

    def clean(self):
        cleaned_data = super().clean()

        user = cleaned_data.get('user')
        venue = cleaned_data.get('venue')

        if user and venue:
            if VenueManager.objects.filter(venue=venue, user=user).exists():
                raise forms.ValidationError(
                    'Venue manager already exists.')
