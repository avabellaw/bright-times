from django.urls import path

from . import views

urlpatterns = [
    # Buy a ticket
    path('buy-ticket/<int:event_id>/', views.buy_ticket, name='buy-ticket'),

    # Buy ticket page
    path('create-payment-intent/', views.create_payment_intent,
         name='create-payment-intent'),

    # Stripe checkout
    path('checkout/', views.checkout, name='checkout'),
    path('checkout-success/', views.checkout_success, name='checkout-success'),
    path('create-order/', views.create_order, name='create-order'),
]
