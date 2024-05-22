from django.urls import path
from . import views

urlpatterns = [
    path('venue-management/', views.venue_management, name='venue-management'),
]
