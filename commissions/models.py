from django.db import models
from accounts.models import Profile 


class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Commission Types"

    def __str__(self):
        return self.name


class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.ForeignKey(
        CommissionType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    people_required = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('Open', 'Open'),
            ('Full', 'Full')
        ],
        default='Open'
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]
        verbose_name_plural = "Commissions"
    
    def __str__(self):
        return self.title


class Job(models.Model):
    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE
    )
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('Open', 'Open'),
            ('Full', 'Full')
        ],
        default='Open'
    )

    class Meta:
        ordering = ['status', '-manpower_required' 'role']
    
    def __str__(self):
        return self.role
    

class JobApplication(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )
    applicant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Accepted', 'Accepted'),
            ('Rejected', 'Rejected')
        ]
        default="Pending"
    )
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['status', '-applied_on']

    def __str__(self):
        return str(self.applicant)


