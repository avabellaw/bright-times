from django.test import TestCase
from .models import Venue, VenueManager, Address, Event
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone


date_now = timezone.now()
date_future = date_now + timedelta(days=7)
date_future_day_before = date_future - timedelta(days=1)
date_future_plus_week = date_future + timedelta(days=7)


class EventTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jane', password='doe')
        self.venue = Venue(address=get_generic_address(), name='Test Venue',
                           capacity=1)
        self.venue.save(created_by=self.user)

    def test_event_created(self):
        event = Event(venue=self.venue, name='Test Event',
                      desc='Test Description', price=1.00,
                      image_url='http://www.test.com',
                      ticket_end_date_time=date_future_day_before,
                      start_date_time=date_future,
                      end_date_time=date_future_plus_week)
        event.save(created_by=self.user)

        self.assertIsNotNone(event)


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
