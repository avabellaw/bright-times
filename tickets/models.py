from django.db import models
from django.contrib.auth.models import User
from events.models import Event
from django.core.validators import MinValueValidator, MaxValueValidator


class Ticket(models.Model):
    order_id = models.ForeignKey('TicketOrder', on_delete=models.CASCADE,
                                 null=False, blank=False, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class TicketOrder(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(max_length=100, blank=False, null=False)
    payment_intent = models.CharField(max_length=500, blank=False, null=False)
    # Quantity, price and order_total are for redundancy
    # Add validators from stackoverflow: [https://stackoverflow.com/questions/849142/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model]
    quantity = models.IntegerField(blank=False, null=False,
                                   validators=[MinValueValidator(1),
                                               MaxValueValidator(10)])
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False,
                                null=False)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      blank=False, null=False)
