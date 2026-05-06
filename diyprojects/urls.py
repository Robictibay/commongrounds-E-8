from django.urls import path
from .views import ProjectListView, ProjectDetailView, ProjectCreateView, ProjectUpdateView


urlpatterns = [
    path("projects", ProjectListView.as_view(), name="project-list"),
    path("project/add", 
         ProjectCreateView.as_view(), name="project-create"),
    path("project/<int:pk>", 
         ProjectDetailView.as_view(), name="project-detail"),
    path("project/<int:pk>/edit", 
         ProjectUpdateView.as_view(), name="project-update"),
]

app_name = "diyprojects"
