from django.contrib import admin
from .models import Genre, Book


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',
                    'publication_year', 'created_on', 'updated_on')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', )
