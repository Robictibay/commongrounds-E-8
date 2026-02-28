from django.db import models

class EventType(models.Model):
    name = models.CharField(max_length=255) # [cite: 57]
    description = models.TextField() # [cite: 58]

    class Meta:
        ordering = ['name'] # [cite: 59]

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=255) # [cite: 60]
    category = models.ForeignKey(
        EventType, 
        on_delete=models.SET_NULL, 
        null=True
    ) # [cite: 61]
    description = models.TextField() # [cite: 61]
    location = models.CharField(max_length=255) # [cite: 62]
    start_time = models.DateTimeField() # [cite: 63]
    end_time = models.DateTimeField() # [cite: 64]
    
    #  auto_now_add=True only sets when created
    created_on = models.DateTimeField(auto_now_add=True) 
    #  auto_now=True updates on every save
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on'] # 

    def __str__(self):
        return self.title