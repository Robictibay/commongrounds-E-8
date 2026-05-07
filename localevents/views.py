from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from accounts.mixins import RoleRequiredMixin
from .models import Event, EventSignup
from .forms import EventForm


class EventListView(ListView):
    model = Event
    template_name = 'localevents/event_list.html'
    context_object_name = 'events'


class EventDetailView(DetailView):
    model = Event
    template_name = 'localevents/event_detail.html'
    context_object_name = 'event'


class EventCreateView(RoleRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'localevents/event_form.html'
    required_role = 'Event Organizer'

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.organizer.add(self.request.user.profile)
        return response


class EventUpdateView(RoleRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'localevents/event_form.html'
    required_role = 'Event Organizer'

    def form_valid(self, form):
        if form.instance.status not in ['Cancelled', 'Done']:
            if self.object.eventsignup_set.count() >= form.instance.event_capacity:
                form.instance.status = 'Full'
            else:
                form.instance.status = 'Available'

        return super().form_valid(form)


def signup_for_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        if event.status != 'Available':
            return redirect('localevents:event-detail', pk=pk)

        if request.user.is_authenticated:
            already_registered = EventSignup.objects.filter(
                event=event,
                user_registrant=request.user.profile
            ).exists()

            if not already_registered:
                EventSignup.objects.create(event=event, user_registrant=request.user.profile)
        else:
            guest_name = request.POST.get('new_registrant')
            if guest_name:
                EventSignup.objects.create(event=event, new_registrant=guest_name)

        if event.eventsignup_set.count() >= event.event_capacity:
            event.status = 'Full'
            event.save()

    return redirect('localevents:event-detail', pk=pk)
