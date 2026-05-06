from django.contrib import admin

from .models import Product, ProductType, Transaction


class ProductAdmin(admin.ModelAdmin):
    model = Product
    search_fields = ('name', 'product_type')
    list_display = ('name', 'owner', 'product_type', 'description', 'price',
                    'stock', 'status')
    list_filter = ('product_type',)


class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    search_fields = ('name',)
    list_display = ('name', 'description',)


class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    search_fields = ('buyer', 'product')
    list_display = ('buyer', 'product', 'amount', 'status', 'created_on')
    list_filter = ('buyer', 'product', 'status')


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Transaction, TransactionAdmin)
