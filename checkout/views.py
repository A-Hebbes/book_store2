from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from bookshelf.contexts import bookshelf_contents

import stripe

def checkout(request):
    bookshelf = request.session.get('bookshelf', {})
    if not bookshelf:
        messages.error(request, "Your bookshelf is empty at the moment")
        return redirect(reverse('books'))
    
    current_bookshelf = bookshelf_contents(request)
    total = current_bookshelf['grand_total']
    stripe_total = round(total * 100)

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51Q5EeK00Qa65K0ZpaITJ0e4Dmm7zZa9GXfMVQgwiQKI4uKW8PQFRrAF3Wyby00qxcpknP0crUHkqA0Nb3kFTRDyd00mdiV69NA'
    }

    return render(request, template, context)