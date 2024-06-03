from django.db import models
from django.contrib.auth.models import User
from events.models import Event
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Ticket(models.Model):
    order = models.ForeignKey('TicketOrder', on_delete=models.CASCADE,
                              null=False, blank=False,
                              related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class TicketOrder(models.Model):
    order_num = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                 editable=False, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    # 32-64 characters is recommended by Stripe incase the size is increased
    payment_intent = models.CharField(max_length=64, blank=False, null=False)
    # Quantity, price and order_total are for redundancy
    # Add validators from stackoverflow: [https://stackoverflow.com/questions/849142/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model]
    quantity = models.IntegerField(blank=False, null=False,
                                   validators=[MinValueValidator(1),
                                               MaxValueValidator(10)])
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False,
                                null=False)

    def get_total(self):
        return self.quantity * self.price
