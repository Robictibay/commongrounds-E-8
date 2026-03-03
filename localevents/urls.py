from django.urls import path
from .views import EventListView, EventDetailView

urlpatterns = [
    # PDF Spec: /localevents/events [cite: 52]
    path('events', EventListView.as_view(), name='event-list'), 
    # PDF Spec: /localevents/event/1 [cite: 53]
    path('event/<int:pk>', EventDetailView.as_view(), name='event-detail'), 
]