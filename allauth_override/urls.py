from django.urls import path

from . import views

urlpatterns = [
    path('verified-email-required/', views.verified_email_required,
         name='verified-email-required'),
]
