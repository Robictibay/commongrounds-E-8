from django.urls import path
from .views import ProductListView, ProductDetailView

app_name = "merchstore"

urlpatterns = [
    path('items', ProductListView.as_view(), name='item-list'),
    path('item/<int:pk>', ProductDetailView.as_view(), name='item-detail')
]
