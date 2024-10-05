from django import forms
from .models import Book, BOOK_CATEGORIES


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'price', 'category', 'description', 'image_path']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = BOOK_CATEGORIES
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if isbn is not None and len(isbn) != 13:
            raise forms.ValidationError("ISBN must be 13 characters long.")
        return isbn
"""
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if len(isbn) != 13:
            raise forms.ValidationError("ISBN must be 13 characters long.")
        return isbn
"""


