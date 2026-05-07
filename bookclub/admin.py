from django.contrib import admin
from .models import Genre, Book, BookReview, Bookmark, Borrow


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'contributor', 'publication_year', 'available_to_borrow')
    list_filter = ('genre', 'available_to_borrow')
    search_fields = ('title', 'author')


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'book', 'user_reviewer', 'anon_reviewer')
    list_filter = ('book',)
    search_fields = ('title', 'comment')


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('profile', 'book', 'date_bookmarked')
    list_filter = ('book',)


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrower', 'name', 'date_borrowed', 'date_to_return')
    list_filter = ('book',)
    search_fields = ('name',)
