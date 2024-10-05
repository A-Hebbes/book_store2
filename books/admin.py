from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = (
         'title',
        'author',
        'isbn',
        'category',
        'price',
        'image',
    )
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Book, BookAdmin)
