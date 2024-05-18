from django.urls import path

from . import views

urlpatterns = [
    # Buy a ticket
    path('ticket/<int:event_id>', views.buy_ticket, name='buy_ticket'),
]
