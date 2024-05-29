from django.shortcuts import render


def verified_email_required(request):
    return render(request, 'account/verified-email-required.html')
