from django.db import models
from django.urls import reverse

# Create your models here.


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        related_name='product',
        null=True
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        return reverse('merchstore:item-detail', args=[str(self.id)])
