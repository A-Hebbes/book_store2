from django.shortcuts import render
from .models import Book

# Create your views here.
def all_books(request):
    """ view to show all books including sortiing and search queries """

    books = Book.objects.all()

    context = {
        'books' : books,
    }
    return render(request, 'books/books.html', context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})