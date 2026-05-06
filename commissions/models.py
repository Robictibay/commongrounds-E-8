from django.db import models


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

