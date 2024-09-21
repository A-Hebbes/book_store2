from django.shortcuts import render


def view_bookshelf(request):
    """ View to render bookshelf page """

    return render(request, 'bookshelf/bookshelf.html')
