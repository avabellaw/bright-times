from django.shortcuts import render


def checkout(request):

    template = 'payments/checkout.html'

    return render(request, template)
