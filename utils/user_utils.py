from allauth.account.admin import EmailAddress


def has_a_verified_email(request):
    """Return whether email has been verified.

    From stackoverflow post [https://stackoverflow.com/questions/54467321/how-to-tell-if-users-email-address-has-been-verified-using-django-allauth-res]
    """
    return EmailAddress.objects.filter(user=request.user,
                                       verified=True).exists()
