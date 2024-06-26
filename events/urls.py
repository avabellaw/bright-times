from django.urls import path
from . import views

urlpatterns = [
    path('', views.events, name='events'),

    # Create an event
    path('create/<int:venue_id>/', views.create_event, name='create-event'),

    # Select venue and go to event creation page
    path('select-venue/', views.select_venue,
         name='select-venue'),

    # Get choose or create venue page
    path('choose-or-create-venue/',
         views.choose_or_create_venue,
         name='choose-or-create-venue'),

    # Event details
    path('event-details/<int:event_id>/', views.event_details,
         name='event-details'),
]
