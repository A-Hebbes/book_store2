from django import forms
from .widgets import CustomClearableFileInput
from django.utils.text import slugify
from .models import Book, BOOK_CATEGORIES


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'isbn', 'price',
            'category', 'description', 'image'
        ]

    category = forms.ChoiceField(choices=BOOK_CATEGORIES)
    image = forms.ImageField(
        label='Image',
        required=False,
        widget=CustomClearableFileInput
    )

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
            instance.image_path = f"books/{self.cleaned_data['image'].name}"

        # Generate a unique slug
        base_slug = slugify(instance.title)
        unique_slug = base_slug
        num = 1
        while Book.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{num}"
            num += 1
        instance.slug = unique_slug

        if commit:
            instance.save()
        return instance
