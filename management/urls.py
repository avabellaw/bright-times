from django.urls import path
from . import views

urlpatterns = [
    # Venue managament urls
    path('venue-management/', views.venue_management, name='venue-management'),

    path('venue-management/venue-detail/<int:venue_id>',
         views.venue_detail, name='venue-management-detail'),

    path('venue-management/delete-venue/<int:venue_id>',
         views.delete_venue, name='delete-venue'),

    # Event management urls
    path('event-management/', views.event_management, name='event-management'),

    path('event-management/event-detail/<int:event_id>',
         views.event_detail, name='event-management-detail'),

    path('event-management/delete-event/<int:event_id>',
         views.delete_event, name='delete-event'),
]
