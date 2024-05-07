from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User


class Event(models.Model):
    venue = models.ForeignKey("Venue", null=False, blank=False,
                              on_delete=models.CASCADE)
    created_by_venue_manager = models.ForeignKey("VenueManager",
                                                 on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=50)
    desc = models.CharField(blank=False, null=False, max_length=1000)
    price = models.DecimalField(blank=False, null=False,
                                max_digits=4, decimal_places=2)
    image_url = models.CharField(blank=False, null=False, max_length=100)
    created_on = models.DateField(auto_now_add=True)
    ticket_end_date_time = models.DateTimeField(blank=False, null=False,
                                                auto_now=False,
                                                auto_now_add=False)
    start_date_time = models.DateTimeField(blank=False, null=False,
                                           auto_now=False, auto_now_add=False)
    end_date_time = models.DateTimeField(blank=False, null=False,
                                         auto_now=False, auto_now_add=False)

    def save(self, created_by=None, *args, **kwargs):
        """
        Overide the save method

        If the event is being created, set the created_by attribute to the 
        the venue manager who created the event.        
        """

        try:
            self.created_by
        except AttributeError:
            self.created_by = created_by

        if not self.pk:
            self.created_by_venue_manager = VenueManager.objects.get(
                                                       venue=self.venue,
                                                       user=self.created_by
                                                    )

        super().save(*args, **kwargs)


class Venue(models.Model):
    address = models.ForeignKey('Address', null=True, blank=False,
                                on_delete=models.SET_NULL)
    name = models.CharField(blank=False, null=False, max_length=50)
    capacity = models.IntegerField(blank=False, null=False)

    managers = models.ManyToManyField(User, through='VenueManager')

    def __str__(self):
        return f'{self.name} - "{self.address}"'

    def save(self, created_by=None, *args, **kwargs):
        """Override the save method to create the original VenueManager

        The attribute created_by is passed in by the test case. 
        Otherwise created_by is blank.
        """

        just_created = not self.pk

        # Save the Venue
        super().save(*args, **kwargs)

        try:
            self.created_by
        except AttributeError:
            self.created_by = created_by

        # Create venue manager if just created
        if just_created:
            VenueManager.objects.create(user=self.created_by, venue=self)


class VenueManager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)


class Address(models.Model):
    class Meta:
        verbose_name_plural = "Addresses"

    street_address1 = models.CharField(blank=False, null=False,
                                       max_length=40)
    street_address2 = models.CharField(blank=True, null=True,
                                       max_length=40)
    city = models.CharField(blank=False, null=False, max_length=100)
    postcode = models.CharField(blank=False, null=False, max_length=20)
    county = models.CharField(blank=False, null=False, max_length=100)
    country = CountryField(blank_label="(select country)",
                           blank=False, null=False)

    def __str__(self):
        return f'{self.street_address1}, \
                {self.city}, {self.postcode}, {self.country}'


def get_venue_attached_to_address(address):
    venues = Venue.objects.filter(address=address)
    if venues.count() > 1:
        venues = f'[Multiple Venues: {venues}]'
    elif venues.count() == 1:
        venues = f'[Venue: {venues.first().name}]'
    else:
        venues = '[No Venue]'
    return venues
