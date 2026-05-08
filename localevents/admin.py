from django.contrib import admin
from .models import EventType, Event, EventSignup

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_time', 'created_on')
    list_filter = ('category',)
    search_fields = ('title', 'description', 'location')

# Add the missing model
admin.site.register(EventSignup)