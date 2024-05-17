from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    street_address1 = models.CharField(blank=True, null=True,
                                       max_length=40)
    street_address2 = models.CharField(blank=True, null=True,
                                       max_length=40)
    city = models.CharField(blank=True, null=True, max_length=100)
    postcode = models.CharField(blank=True, null=True, max_length=20)
    county = models.CharField(blank=True, null=True, max_length=100)
    country = CountryField(blank_label="(select country)",
                           blank=True, null=True)
