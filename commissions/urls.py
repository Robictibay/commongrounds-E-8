from django.urls import path
from .views import commission_specific, commission_list

app_name = "commissions"
urlpatterns = [
    path("requests", commission_list, name="commission_list"),
    path("request/<int:pk>", commission_specific, name="commission_specific"),

]
