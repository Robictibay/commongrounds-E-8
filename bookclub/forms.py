from django import forms
from datetime import timedelta, date
from .models import Book, BookReview, Borrow, Genre


class BookCreateForm(forms.ModelForm):
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        empty_label="Select a Genre"
    )

    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'synopsis', 'publication_year', 'available_to_borrow']
        widgets = {
            'publication_year': forms.NumberInput(attrs={'min': 1})
        }


class BookUpdateForm(forms.ModelForm):
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        empty_label="Select a Genre"
    )

    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'synopsis', 'publication_year', 'available_to_borrow']
        widgets = {
            'publication_year': forms.NumberInput(attrs={'min': 1})
        }


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['title', 'comment']


class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['name', 'date_borrowed']
        widgets = {
            'date_borrowed': forms.DateInput(attrs={'type': 'date'})
        }

    def clean(self):
        cleaned_data = super().clean()
        date_borrowed = cleaned_data.get('date_borrowed')

        if date_borrowed:
            if date_borrowed < date.today():
                raise forms.ValidationError('Borrow date cannot be before today.')
            cleaned_data['date_to_return'] = date_borrowed + timedelta(weeks=2)

        return cleaned_data
