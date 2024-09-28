from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from django.urls import reverse
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
    else:
        bookshelf[book_id] = quantity
       

    request.session['bookshelf'] = bookshelf
    return redirect(redirect_url)

"""
def remove_from_bookshelf(request, book_id):
    
    bookshelf = request.session.get('bookshelf', {})

    if str(book_id) in bookshelf:
        del bookshelf[str(book_id)]
        request.session['bookshelf'] = bookshelf
        messages.success(request, "Removed book from your bookshelf")

    # Recalculate totals
    total = sum(get_object_or_404(Book, book_id=int(id)).price * qty for id, qty in bookshelf.items())
    delivery = calculate_delivery(total) 
    grand_total = total + delivery



    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'new_total': total,
            'new_delivery': delivery,
            'new_grand_total': grand_total,
            'bookshelf_items_count': len(bookshelf)
            })
    else:
        return redirect(reverse('view_bookshelf'))

"""

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
        bookshelf.pop[book_id]

    request.session['bookshelf'] = bookshelf

    return redirect(reverse('view_bookshelf'))