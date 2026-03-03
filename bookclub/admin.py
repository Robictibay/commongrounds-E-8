from django.contrib import admin
from .models import Genre, Book

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # This shows the most important info in the admin list view
    list_display = ('title', 'author', 'publication_year', 'created_on', 'updated_on')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', )
