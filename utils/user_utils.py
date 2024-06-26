from allauth.account.admin import EmailAddress


def get_primary_email(request):
    """Get primary email of user.

    args:
        request: Request object.

    Returns:
        str: Primary email of user.
    """
    return EmailAddress.objects.get(user=request.user, primary=True,
                                    verified=True).email


def has_a_verified_email(request):
    """Get whether email has been verified.

    From stackoverflow post [https://stackoverflow.com/questions/54467321/how-to-tell-if-users-email-address-has-been-verified-using-django-allauth-res]
    """
    return EmailAddress.objects.filter(user=request.user,
                                       verified=True).exists()


def is_email_verified(request, email):
    """Return whether specific email has been verified.

    args:
        request: Request object.
        email: Email to check.

    Returns:
        bool: Whether email has been verified. False if doesn't belong to user.
    """
    return EmailAddress.objects.filter(user=request.user,
                                       email=email,
                                       verified=True).exists()
