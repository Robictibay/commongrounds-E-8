from django.urls import path
from .views import commission_specific, commission_list, commission_create, commission_update

app_name = "commissions"
urlpatterns = [
    path("requests", commission_list, name="commission_list"),
    path("request/<int:pk>", commission_specific, name="commission_specific"),
    path("request/add", commission_create, name="commission_create"),
    path("request/<int:pk>/edit", commission_update, name="commission_update")

]
