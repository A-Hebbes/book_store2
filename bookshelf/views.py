from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from books.models import Book

def view_bookshelf(request):
    """ View to render bookshelf page """
    bookshelf = request.session.get('bookshelf', {})
    bookshelf_items = []

    for book_id, quantity in bookshelf.items():
        book = get_object_or_404(Book, book_id=int(book_id))
        bookshelf_items.append({
            'book': book,
            'quantity': quantity,
        })

    context = {
        'bookshelf_items': bookshelf_items,
    }

    return render(request, 'bookshelf/bookshelf.html', context)

def add_to_bookshelf(request, book_id):
    """ Add a quantity of the book to the bookshelf """
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bookshelf = request.session.get('bookshelf', {})

    if str(book_id) in list(bookshelf.keys()):
        bookshelf[str(book_id)] += quantity
    else:
        bookshelf[str(book_id)] = quantity

    request.session['bookshelf'] = bookshelf
    return redirect(redirect_url)

def remove_from_bookshelf(request, book_id):
    """Remove the book from the bookshelf"""
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


def adjust_bookshelf(request, book_id):
    """Adjust the quantity """
    quantity = int(request.POST.get('quantity'))
    bookshelf = request.session.get('bookshelf', {})

    if quantity > 0:
        bookshelf[str(book_id)] = quantity
    else:
        bookshelf.pop(str(book_id))

    request.session['bookshelf'] = bookshelf
    messages.success(request, "Updated bookshelf quantity")
    return redirect(reverse('view_bookshelf'))