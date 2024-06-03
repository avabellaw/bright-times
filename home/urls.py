from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('.well-known/apple-developer-merchantid-domain-association',
         views.verify_stripe, name='verify_stripe'),
]
