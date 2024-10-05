from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Book, BOOK_CATEGORIES
from .forms import BookForm

def all_books(request):
    books = Book.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'title':
                sortkey = 'lower_title'
                books = books.annotate(lower_title=Lower('title'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            books = books.order_by(sortkey)
        
        if 'category' in request.GET:
            categories = [cat.strip() for cat in request.GET['category'].split(',')]
            books = books.filter(category__in=categories)

        if 'price_category' in request.GET:
            price_category = request.GET['price_category']
            if price_category == 'premium':
                books = books.filter(price__gte=15)  
            elif price_category == 'budget':
                books = books.filter(price__lt=10) 

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You did not enter a valid search")
                return redirect(reverse('all_books'))

            queries = Q(title__icontains=query) | Q(author__icontains=query) | \
                      Q(description__icontains=query) | Q(category__icontains=query) | \
                      Q(isbn__icontains=query)
            books = books.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'books': books,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'all_categories': dict(BOOK_CATEGORIES).values(),
    }
    return render(request, 'books/books.html', context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    
    context = {
        'book': book,
    }
    return render(request, 'books/book_detail.html', context)

def add_book(request):
    """ Add a book to the store """
    form = BookForm()
    template = 'books/add_book.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
    