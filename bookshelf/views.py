from django.shortcuts import render, redirect


def view_bookshelf(request):
    """ View to render bookshelf page """

    return render(request, 'bookshelf/bookshelf.html')


def add_to_bookshelf(request, book_id):
    """ Add a quantity of the book to the bookshelf """
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bookshelf = request.session.get('bookshelf', {})

    if book_id in list(bookshelf.keys()):
        bookshelf[book_id] += quantity
    else:
        bookshelf[book_id] = quantity

    request.session['bookshelf'] = bookshelf
    print(request.session['bookshelf'])
    return redirect(redirect_url)