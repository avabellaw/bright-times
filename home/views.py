from django.shortcuts import render


def home(request):
    """View for homepage"""
    return render(request, 'home/index.html')
