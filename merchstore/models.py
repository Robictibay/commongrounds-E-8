from django.db import models
from django.urls import reverse
from accounts.models import Profile

# Create your models here.


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)


class Product(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('On sale', 'On sale'),
        ('Out of stock', 'Out of stock'),
    ]
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        related_name='product',
        null=True
    )
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='product',
        null=True
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    status = models.CharField(choices=STATUS_CHOICES, default='Available')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        return reverse('merchstore:item-detail', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        if self.stock == 0:
            self.status = 'Out of stock'
        else:
            self.status = 'Available'
        super().save(*args, **kwargs)


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('On cart', 'On cart'),
        ('To Pay', 'To Pay'),
        ('To Ship', 'To Ship'),
        ('To Receive', 'To Receive'),
        ('Delivered', 'Delivered'),
    ]
    buyer = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name='transaction',
        null=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='transaction'
    )
    amount = models.PositiveIntegerField()
    status = models.CharField(choices=STATUS_CHOICES, default='On cart')
    created_on = models.DateTimeField(auto_now_add=True)
