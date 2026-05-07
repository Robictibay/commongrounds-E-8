from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookBorrowView


urlpatterns = [
    path('books', BookListView.as_view(), name='book-list'),
    path('book/<int:pk>', BookDetailView.as_view(), name='book-detail'),
    path('book/add', BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/edit', BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/borrow', BookBorrowView.as_view(), name='book-borrow'),
]

app_name = 'bookclub'
