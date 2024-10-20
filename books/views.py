from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import superuser_required
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
            categories = request.GET['category'].split(',')
            categories = [cat.strip() for cat in categories]
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

            queries = (Q(title__icontains=query) |
                       Q(author__icontains=query) |
                       Q(description__icontains=query) |
                       Q(category__icontains=query) |
                       Q(isbn__icontains=query))
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


@login_required
@superuser_required
def add_book(request):
    """ Add a book to the store """
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, 'Your Book Has Been Added')
            return redirect(reverse('book_detail', args=[book.book_id]))
        else:
            messages.error(
                request,
                'Your Book was not updated. Check the form and resubmit'
            )
    else:
        form = BookForm()

    template = 'books/add_book.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
@superuser_required
def edit_book(request, book_id):
    """ Edit a book in the store """
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'The book has been updated')
            return redirect(reverse('book_detail', args=[book.book_id]))
        else:
            messages.error(
                request,
                'Your book was not updated. Check the form and resubmit'
            )
    else:
        form = BookForm(instance=book)
        messages.info(request, f'You are editing {book.title}')

    template = 'books/edit_book.html'
    context = {
        'form': form,
        'book': book,
    }
    return render(request, template, context)


@login_required
@superuser_required
def delete_book(request, book_id):
    """ Delete a book from the store """
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    messages.success(request, 'The book has been deleted')
    return redirect(reverse('all_books'))
