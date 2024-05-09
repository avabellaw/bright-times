from django.urls import path
from . import views

urlpatterns = [
    path('', views.events, name='events'),
    path('create/', views.create_event, name='create_event'),
    path('choose-or-create-venue/', views.choose_or_create_venue,
         name='choose_or_create_venue'),
]
