from django.contrib import admin

from .models import Ticket, TicketOrder

admin.site.register(Ticket)
admin.site.register(TicketOrder)
