from django.urls import path
from . import views

urlpatterns = [
    path('', views.events, name='events'),

    # Create an event
    path('create/<int:venue_id>', views.create_event, name='create_event'),

    # Select venue and go to event creation page
    path('select-venue/', views.select_venue_and_create_event,
         name='select_venue'),

    # Choose or create a venue
    path('choose-or-create-venue/<str:create_venue>/',
         views.choose_or_create_venue,
         name='choose_or_create_venue'),

    # Get choose or create venue page
    path('choose-or-create-venue/',
         views.choose_or_create_venue,
         name='choose_or_create_venue'),

    # Buy a ticket
    path('buy-ticket/<int:event_id>', views.buy_ticket, name='buy-ticket'),

    # Event details
    path('event-details/<int:event_id>', views.event_details,
         name='event-details'),
]
