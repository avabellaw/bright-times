from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from events.tests import create_test_event, get_generic_address
from events.models import Venue
from .models import Ticket
from django.shortcuts import reverse
from django.conf import settings


class TicketTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jane', password='doe')
        self.user.save()
        self.venue = Venue(address=get_generic_address(),
                           name='Test Venue', capacity=1)
        self.venue.save(created_by=self.user)
        self.event = create_test_event(self.venue, self.user)

        self.client = Client()

        self.client.login(username=self.user.username, password='doe')

    def test_can_user_buy_ticket(self):
        self.client.post(reverse('buy-ticket', args=[self.event.id]),
                         data={'quantity': '1'})

        ticket_count = Ticket.objects.filter(event=self.event,
                                             user=self.user).count()

        self.assertEqual(ticket_count, 1)

    def test_user_cannot_buy_more_than_max_tickets(self):
        max_tickets = settings.MAX_TICKETS_PER_USER
        self.client.post(reverse('buy-ticket', args=[self.event.id]),
                         data={'quantity': f'{max_tickets + 1}'})

        ticket_count = Ticket.objects.filter(event=self.event,
                                             user=self.user).count()

        self.assertEqual(ticket_count, 0)

    def test_user_cannot_buy_more_than_max_ticket_overall(self):
        max_tickets = settings.MAX_TICKETS_PER_USER
        self.client.post(reverse('buy-ticket', args=[self.event.id]),
                         data={'quantity': f'{max_tickets}'})

        self.client.post(reverse('buy-ticket', args=[self.event.id]),
                         data={'quantity': '1'})

        ticket_count = Ticket.objects.filter(event=self.event,
                                             user=self.user).count()

        self.assertEqual(ticket_count, max_tickets)
