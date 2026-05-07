from django.urls import path
from .views import (ProductListView, ProductDetailView, ProductCreateView,
                    ProductUpdateview, CartView, TransactionsList)

app_name = "merchstore"

urlpatterns = [
    path('items', ProductListView.as_view(), name='item-list'),
    path('item/<int:pk>', ProductDetailView.as_view(), name='item-detail'),
    path('item/add', ProductCreateView.as_view(), name='item-add'),
    path('item/<int:pk>/edit', ProductUpdateview.as_view(), name='item-edit'),
    path('cart', CartView.as_view(), name='cart-view'),
    path('transactions', TransactionsList.as_view(), name='transaction-list'),
]
