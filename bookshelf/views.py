from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from books.models import Book


def view_bookshelf(request):
    """ A view to render bookshelf contents """
    return render(request, 'bookshelf/bookshelf.html')


def add_to_bookshelf(request, book_id):
    """ Add a quantity of the book to the bookshelf """
    book = get_object_or_404(Book, pk=book_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bookshelf = request.session.get('bookshelf', {})

    if book_id in list(bookshelf.keys()):
        bookshelf[book_id] += quantity
        messages.success(
            request,
            f'Updated quantity of {book.title} to {bookshelf[book_id]}'
        )
    else:
        bookshelf[book_id] = quantity
        messages.success(request, f'Added {book.title} to your bookshelf')

    request.session['bookshelf'] = bookshelf
    return redirect(redirect_url)


def remove_from_bookshelf(request, book_id):
    """Remove the book from the bookshelf"""
    try:
        book = get_object_or_404(Book, pk=book_id)
        bookshelf = request.session.get('bookshelf', {})

        bookshelf.pop(str(book_id))
        messages.success(request, f'Removed {book.title} from your bookshelf')

        request.session['bookshelf'] = bookshelf
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing book: {e}')
        return HttpResponse(status=500)


def adjust_bookshelf(request, book_id):
    """Adjust the quantity """
    quantity = int(request.POST.get('quantity'))
    bookshelf = request.session.get('bookshelf', {})

    if quantity > 0:
        bookshelf[book_id] = quantity
    else:
        bookshelf.pop(book_id)

    request.session['bookshelf'] = bookshelf

    return redirect(reverse('view_bookshelf'))
