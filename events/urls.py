from django.urls import path
from . import views

urlpatterns = [
    path('', views.events, name='events'),
    path('create/', views.create_event, name='create_event'),
]
