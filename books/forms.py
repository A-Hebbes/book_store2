from django import forms
from .models import Book, BOOK_CATEGORIES

class BookForm(forms.ModelForm):
    image = forms.ImageField(label='Image', required=False)
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'price', 'category', 'description']
    
    category = forms.ChoiceField(choices=BOOK_CATEGORIES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if isbn is not None and len(isbn) != 13:
            raise forms.ValidationError("ISBN must be 13 characters long.")
        return isbn

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('image'):
            # Handle the image file and set image_path
            # This part depends on how you want to store and name your files
            instance.image_path = f"books/{self.cleaned_data['image'].name}"
        if commit:
            instance.save()
        return instance


"""
OLD BOOK FORM COMMENTED TO TEST FOR IMAGE UPLOAD
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



