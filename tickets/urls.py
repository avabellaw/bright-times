from django.urls import path

from . import views

urlpatterns = [
    # Buy a ticket
    path('buy-ticket/<int:event_id>/', views.buy_ticket, name='buy-ticket'),

    # Buy ticket page
    path('create-payment-intent/', views.create_payment_intent,
         name='create-payment-intent'),

    # Show user tickets
    path('my-tickets/', views.user_tickets, name='user-tickets'),

    # Stripe checkout
    path('checkout/', views.checkout, name='checkout'),
    path('checkout-success/<str:order_num>', views.checkout_success,
         name='checkout-success'),
    path('create-order/', views.create_order, name='create-order'),
]
