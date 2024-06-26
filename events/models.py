from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.conf import settings


class Event(models.Model):
    venue = models.ForeignKey("Venue", null=False, blank=False,
                              on_delete=models.CASCADE)
    created_by_venue_manager = models.ForeignKey("VenueManager",
                                                 on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=50)
    desc = models.CharField(blank=False, null=False, max_length=300)
    about = models.TextField(blank=False, null=False, max_length=1500)
    price = models.DecimalField(blank=False, null=False,
                                max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to='event_images/',
                              blank=False, null=False)
    created_on = models.DateField(auto_now_add=True)
    ticket_end_date_time = models.DateTimeField(blank=False, null=False,
                                                auto_now=False,
                                                auto_now_add=False)
    start_date_time = models.DateTimeField(blank=False, null=False,
                                           auto_now=False, auto_now_add=False)
    end_date_time = models.DateTimeField(blank=False, null=False,
                                         auto_now=False, auto_now_add=False)

    def get_tickets_sold(self):
        from tickets.models import Ticket
        return Ticket.objects.filter(event=self).count()

    def get_tickets_left(self):
        num_of_tickets_sold = self.get_tickets_sold()
        return self.venue.capacity - num_of_tickets_sold

    def __str__(self):
        return f'{self.name}, at {self.venue.name}'

    def save(self, created_by=None, *args, **kwargs):
        """
        Overide the save method

        If the event is being created, set the created_by attribute to the
        the venue manager who created the event.
        """

        self.created_by = created_by

        # If event was just created, set the created_by field
        if not self.pk:
            check_created_by_is_set(created_by)

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

        # Create venue manager if just created
        if just_created:
            check_created_by_is_set(created_by)

            VenueManager.objects.create(user=created_by,
                                        venue=self,
                                        role=settings.VENUE_MANAGER_ROLE[0])


def check_created_by_is_set(created_by):
    if created_by is None:
        raise ValueError('created_by must be passed as an arugment \
            when creating a venue.')


class VenueManager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return f'{self.venue.name} {self.role.lower()}: {self.user.username}'


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
