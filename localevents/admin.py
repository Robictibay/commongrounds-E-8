from django.contrib import admin
from .models import EventType, Event

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name',) #

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # This shows the most important info in the admin list view
    list_display = ('title', 'category', 'start_time', 'created_on') #
    list_filter = ('category',) #
    search_fields = ('title', 'description', 'location') #