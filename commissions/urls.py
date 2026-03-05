from django.urls import path
from .views import commission_specific, commission_list

urlpatterns = [
    path("requests", commission_list, name="commission_list"),
    path("request/<int:pk>", commission_specific, name="commissions_specific"),
]