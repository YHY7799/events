from django.contrib import admin

from .models import Venue
from .models import myuser
from .models import Event


# admin.site.register(Venue)
admin.site.register(myuser)
#admin.site.register(Event)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    ordering = ('name',)
    search_fields = ('name', 'address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'event'), 'date', 'description', 'manager', 'approved')
    list_display = ('name', 'date', 'event') # 'event' means 'venue'
    list_filter = ('date', 'event')
    ordering = ('-date',)