from django.contrib import admin
from .models import ProjectCategory, Project
# Register your models here.

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_on', 'updated_on')
    list_filter = ('category',)
    search_fields = ('title', 'description', 'materials', 'steps')