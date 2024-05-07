from django.test import TestCase
from .models import Venue, VenueManager, Address
from django.contrib.auth.models import User


class VenueTestCase(TestCase):
    def setUp(self):
        self.USER = {
            'admin': User.objects.create_superuser(username='admin',
                                                   password='admin'),
            'regular': User.objects.create_user(username='john',
                                                password='doe')
        }

    def test_venue_created(self):
        venue = Venue(address=get_generic_address(),
                      name='Test Venue', capacity=1)
        venue.save(created_by=self.USER['regular'])
        self.assertIsNotNone(venue)

    def test_venuemanager_created_by_admin(self):
        venue = Venue(address=get_generic_address(),
                      name='Test Venue', capacity=1)
        venue.save(created_by=self.USER['admin'])

        venuemanager = VenueManager.objects.get(venue=venue)
        self.assertIsNotNone(venuemanager)


def get_generic_address():
    return Address.objects.create(street_address1='Street1', city='City',
                                  postcode='ee45 9JR', county='CountryLand',
                                  country='GB')
