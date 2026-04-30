from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('permission-denied/', views.permission_denied_view, name='permission-denied'),
    path('<str:username>/', views.ProfileUpdateView.as_view(), name='profile-update'),
]