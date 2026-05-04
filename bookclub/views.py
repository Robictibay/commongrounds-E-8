from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView

from accounts.mixins import RoleRequiredMixin
from datetime import date
from .models import Book, Bookmark, BookReview, Borrow
from .forms import BookCreateForm, BookUpdateForm, BookReviewForm, BorrowForm


class BookListView(ListView):
    model = Book
    template_name = 'bookclub/book_list.html'
    context_object_name = 'books'

    def _get_grouped_books(self, profile):
        return {
            'contributed': Book.objects.filter(contributor=profile),
            'bookmarked': Book.objects.filter(bookmarks__profile=profile),
            'reviewed': Book.objects.filter(reviews__user_reviewer=profile).distinct(),
        }

    def get_queryset(self):
        all_books = Book.objects.all()

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            groups = self._get_grouped_books(profile)

            contributed_pks = groups['contributed'].values_list('pk', flat=True)
            bookmarked_pks = groups['bookmarked'].values_list('pk', flat=True)
            reviewed_pks = groups['reviewed'].values_list('pk', flat=True)

            special_pks = set(contributed_pks) | set(bookmarked_pks) | set(reviewed_pks)

            return all_books.exclude(pk__in=special_pks)

        return all_books
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            groups = self._get_grouped_books(profile)

            context['contributed_books'] = groups['contributed']
            context['bookmarked_books'] = groups['bookmarked']
            context['reviewed_books'] = groups['reviewed']

        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'bookclub/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object

        context['review_form'] = BookReviewForm()
        context['reviews'] = book.reviews.all()
        context['bookmark_count'] = book.bookmarks.count()

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context['is_contributor'] = (book.contributor == profile)
            context['is_bookmarked'] = book.bookmarks.filter(profile=profile).exists()

        return context

    def _handle_bookmark(self, book):
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            bookmark = Bookmark.objects.filter(book=book, profile=profile)
            if bookmark.exists():
                bookmark.delete()
                return
            Bookmark.objects.create(book=book, profile=profile)
        else:
            messages.error(self.request, 'Not logged in')
    
    def _handle_review(self, book):
        form = BookReviewForm(self.request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            if self.request.user.is_authenticated:
                review.user_reviewer = self.request.user.profile
            else:
                review.anon_reviewer = 'Anonymous'
            review.save()
            return None

        return form

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        book = self.object
        action = request.POST.get('action')

        if action == 'bookmark':
            self._handle_bookmark(book)
        elif action == 'review':
            form = self._handle_review(book)
            if form:
                context = self.get_context_data()
                context['review_form'] = form
                return self.render_to_response(context)

        return redirect('bookclub:book-detail', pk=book.pk)


class BookCreateView(RoleRequiredMixin, CreateView):
    required_role = 'Book Contributor'
    model = Book
    form_class = BookCreateForm
    template_name = 'bookclub/book_create.html'
    success_url = reverse_lazy('bookclub:book-list')

    def form_valid(self, form):
        form.instance.contributor = self.request.user.profile
        return super().form_valid(form)


class BookUpdateView(RoleRequiredMixin, UpdateView):
    required_role = 'Book Contributor'
    model = Book
    form_class = BookUpdateForm
    template_name = 'bookclub/book_update.html'

    def get_success_url(self):
        return reverse_lazy('bookclub:book-detail', kwargs={'pk': self.object.pk})


class BookBorrowView(FormView):
    template_name = 'bookclub/book_borrow.html'
    form_class = BorrowForm

    def get_book(self):
        return get_object_or_404(Book, pk=self.kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        book = self.get_book()
        if not book.available_to_borrow:
            return redirect('bookclub:book-detail', pk=book.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.get_book()
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['date_borrowed'].widget.attrs['min'] = date.today().isoformat()
        
        if self.request.user.is_authenticated:
            form.fields['name'].initial = self.request.user.profile.display_name
            form.fields['name'].widget.attrs['readonly'] = True
        return form

    def form_valid(self, form):
        book = self.get_book()
        borrow = form.save(commit=False)
        borrow.book = book

        if self.request.user.is_authenticated:
            borrow.borrower = self.request.user.profile

        borrow.date_to_return = form.cleaned_data['date_to_return']
        borrow.save()
        return redirect('bookclub:book-detail', pk=book.pk)