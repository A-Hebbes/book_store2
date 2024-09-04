from django.shortcuts import render

def index(request):
    """ view to return the index page """
    return render(request, 'bookshop/index.html')

def my_shop(request):
    """ view to return the bookshop page """
    return render(request, 'bookshop/my_shop.html')

def books(request):

    return render(request, 'bookshop/books.html')