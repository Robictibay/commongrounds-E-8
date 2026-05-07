from django.db import models
from django.urls import reverse


class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):
    STATUS_AVAILABLE = 'Available'
    STATUS_FULL = 'Full'
    STATUS_DONE = 'Done'
    STATUS_CANCELLED = 'Cancelled'

    STATUS_CHOICES = [
        (STATUS_AVAILABLE, 'Available'),
        (STATUS_FULL, 'Full'),
        (STATUS_DONE, 'Done'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        EventType,
        on_delete=models.SET_NULL,
        null=True
    )
    # The PDF requires a ManyToMany field for Organizer
    organizer = models.ManyToManyField(
        'accounts.Profile',
        related_name='organized_events',
        blank=True
    )
    event_image = models.ImageField(upload_to='localevents/images/', blank=True, null=True)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_capacity = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_AVAILABLE
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('localevents:event-detail', args=[str(self.id)])


class EventSignup(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_registrant = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    new_registrant = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        if self.user_registrant:
            return f"{self.user_registrant.display_name} - {self.event.title}"
        return f"{self.new_registrant} - {self.event.title}"
