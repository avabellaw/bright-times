from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

ToastMessage = settings.TOAST_MESSAGE


# Learnt how to make decorator from pymeister
# [https://dev.to/pymeister/how-to-create-decorators-in-django-2f8d#:~:text=This%20function%20is%20called%20a%20decorator.&text=Apply%20the%20Decorator%3A%20To%20apply,%22Hello%2C%20World!%22)] noqa
# And have it replace @login_required from stackoverflow
# [https://stackoverflow.com/questions/5678585/django-tweaking-login-required-decorator]
def login_required_message(view_func):
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            ToastMessage.login_required(request)
            return HttpResponseRedirect(reverse('account_login'))
        else:
            return view_func(request, *args, **kwargs)
    return wrapper