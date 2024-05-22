from django.urls import path
from .views import venue_management

urlpatterns = [
    path('venue-management', views.venue_management, name='venue-management'),
]