from django.db import models
from django.contrib.auth.models import User
from events.models import Address
from allauth.account.admin import EmailAddress


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    address = models.OneToOneField(Address, null=True,
                                   on_delete=models.CASCADE)

    def is_email_verified(self):
        """Return whether email has been verified.

        From stackoverflow post [https://stackoverflow.com/questions/54467321/how-to-tell-if-users-email-address-has-been-verified-using-django-allauth-res]
        """
        return EmailAddress.objects.filter(user=self.user,
                                           verified=True).exists()
