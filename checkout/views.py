from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm
from bookshelf.contexts import bookshelf_contents

def checkout(request):
    bookshelf = request.session.get('bookshelf', {})
    if not bookshelf:
        messages.error(request, "Your bookshelf is empty at the moment")
        return redirect(reverse('books'))
    
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
    }

    return render(request, template, context)