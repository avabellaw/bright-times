from django.db import models
from django.contrib.auth.models import User
from events.models import Address


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    address = models.OneToOneField(Address, null=True,
                                   on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, null=True)
