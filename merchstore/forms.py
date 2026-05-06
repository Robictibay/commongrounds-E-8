from django import forms
from django.db import models
from .models import Product, Transaction


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'product_type', 'description', 'price',
            'stock', 'status'
        ]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = [
            'product', 'buyer', 'created_on'
        ]