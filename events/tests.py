from django.test import TestCase
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.test import Client
from django.urls import reverse

from .models import Venue, VenueManager, Address, Event


date_now = timezone.now()
date_future = date_now + timedelta(days=7)
date_future_day_before = date_future - timedelta(days=1)
date_future_plus_week = date_future + timedelta(days=7)


class EventTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jane', password='doe')
        self.user2 = User.objects.create_user(username='john', password='doe')

        self.venue = Venue(address=get_generic_address(), name='Test Venue',
                           capacity=1)
        self.venue.save(created_by=self.user)

        self.venue2 = Venue(address=get_generic_address(), name='Test Venue 2',
                            capacity=2)
        self.venue2.save(created_by=self.user2)

    def test_event_created(self):
        event = create_test_event(self.venue, self.user)

        self.assertIsNotNone(event)

    def test_access_to_event_creation_page(self):
        client = Client()

        client.login(username=self.user.username, password='doe')

        response = client.get(reverse('create-event', args=[self.venue.id]))

        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access_to_event_creation_page(self):
        client = Client()

        response = client.get(reverse('create-event', args=[self.venue.id]))

        # Test is redirected to login page
        self.assertEqual(response.status_code, 302)

        client.login(username=self.user.username, password='doe')

        response = client.get(reverse('create-event', args=[self.venue2.id]))

        # User should not be able to use User2's venue
        self.assertEqual(response.status_code, 403)


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

    def test_venue_manager_created_with_venue(self):
        venue = Venue(address=get_generic_address(),
                      name='Test Venue', capacity=1)
        venue.save(created_by=self.USER['regular'])

        self.assertIsNotNone(VenueManager.objects.get(venue=venue,
                                                      user=self.USER['regular']
                                                      ))

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


def create_test_event(venue, user):
    event = Event(venue=venue,
                  name='Test Event',
                  desc='Test Description',
                  price=1.00,
                  image='default.png',
                  ticket_end_date_time=date_future_day_before,
                  start_date_time=date_future,
                  end_date_time=date_future_plus_week)
    event.save(created_by=user)
    return event
