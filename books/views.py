from django.shortcuts import render
from .models import Book

# Create your views here.
def all_books(request):
    """ view to show all books including sortiing and search queries """

    books = Book.objects.all()

    context = {
        'products' : products,
    }



    return render(request, 'bookshop/books.html', context)