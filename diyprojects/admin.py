from django.contrib import admin
from .models import ProjectCategory, Project, Favorite, ProjectReview, ProjectRating

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_on', 'updated_on')
    list_filter = ('category',)
    search_fields = ('title', 'description', 'materials', 'steps')

admin.site.register(Favorite)
admin.site.register(ProjectReview)
admin.site.register(ProjectRating)