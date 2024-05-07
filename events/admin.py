from django.contrib import admin
from .models import Event, Venue, Address, VenueManager


class VenueAdmin(admin.ModelAdmin):
    """
    Admin class for Venue model
    """
    # Save model from [https://stackoverflow.com/questions/69233313/
    # store-who-updated-django-model-from-admin-site]
    def save_model(self, request, obj, form, change):
        """
        Override save model method to store the user who created it
        """
        if not change:  # If object not being updated, therefore created
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)
    
    
class EventAdmin(admin.ModelAdmin):
    """
    Admin class for Event model
    """
    def save_model(self, request, obj, form, change):
        """
        Override save model method to store the user who created it
        """
        if not change:  # If object not being updated, therefore created
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)


admin.site.register(Event, EventAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Address)
admin.site.register(VenueManager)
