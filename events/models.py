from django.db import models
from django_countries.fields import CountryField


class Venue(models.Model):
    address = models.ForeignKey('Address', null=True, blank=False,
                                on_delete=models.SET_NULL)
    name = models.CharField(blank=False, null=False, max_length=50)
    capacity = models.IntegerField(blank=False, null=False)


class Address(models.Model):
    class Meta:
        verbose_name_plural = "Addresses"

    full_name = models.CharField(blank=False, null=False, max_length=70)
    street_address1 = models.CharField(blank=False, null=False,
                                       max_length=40)
    street_address2 = models.CharField(blank=True, null=True,
                                       max_length=40)
    city = models.CharField(blank=False, null=False, max_length=100)
    postcode = models.CharField(blank=False, null=False, max_length=20)
    country = CountryField(blank_label="(select country)",
                           blank=False, null=False)
    county = models.CharField(blank=False, null=False, max_length=100)

    def __str__(self):
        return f'{self.full_name}, {self.street_address1}, \
                {self.city}, {self.postcode}, {self.country}'
