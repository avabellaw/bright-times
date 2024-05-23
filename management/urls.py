from django.urls import path
from . import views

urlpatterns = [
    path('venue-management/', views.venue_management, name='venue-management'),
    
    path('venue-management/venue-detail/<int:venue_id>',
         views.venue_detail, name='venue-management-detail'),
    
    path('venue-management/delete-venue/<int:venue_id>',
         views.delete_venue, name='delete-venue'),
]
