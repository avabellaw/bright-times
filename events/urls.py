from django.urls import path
from . import views

urlpatterns = [
    path('', views.events, name='events'),

    # Create an event
    path('create/<int:venue_id>', views.create_event, name='create_event'),

    # Choose or create a venue
    path('choose-or-create-venue/<str:create_venue>/',
         views.choose_or_create_venue,
         name='choose_or_create_venue'),

    # Get choose or create venue page
    path('choose-or-create-venue/',
         views.choose_or_create_venue,
         name='choose_or_create_venue'),
]
