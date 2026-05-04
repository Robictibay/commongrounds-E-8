from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from accounts.models import Profile


class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='books'
    )
    contributor = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='books'
    )
    author = models.CharField(max_length=255)
    synopsis = models.TextField(default='')
    publication_year = models.IntegerField(validators=[MinValueValidator(1)])
    available_to_borrow = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publication_year']

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

    def get_absolute_url(self):
        return reverse('bookclub:book-detail', args=[str(self.id)])


class BookReview(models.Model):
    user_reviewer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reviews'
    )
    anon_reviewer = models.TextField()
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.CharField(max_length=255)
    comment = models.TextField()


class Bookmark(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='bookmarks'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    date_bookmarked = models.DateField(auto_now_add=True)


class Borrow(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='borrows'
    )
    borrower = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='borrows'
    )
    name = models.CharField(max_length=255)
    date_borrowed = models.DateField()
    date_to_return = models.DateField()