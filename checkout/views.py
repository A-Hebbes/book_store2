from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from books.models import Book
from bookshelf.contexts import bookshelf_contents

import stripe
import json

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bookshelf': json.dumps(request.session.get('bookshelf', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user.username if request.user.is_authenticated else 'AnonymousUser',
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=str(e), status=400)

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    
    if request.method == 'POST':
        bookshelf = request.session.get('bookshelf', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postal_code': request.POST['postal_code'],
            'city': request.POST['city'],
            'address_line1': request.POST['address_line1'],
            'address_line2': request.POST['address_line2'],
            'county': request.POST['county'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bookshelf = json.dumps(bookshelf)
            order.save()
            for item_id, item_data in bookshelf.items():
                try:
                    book = Book.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            book=book,
                            quantity=item_data,
                        )
                        order_line_item.save()
                except Book.DoesNotExist:
                    messages.error(request, (
                        "One of the books in your bookshelf wasn't found."
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bookshelf'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form.')
    else:
        bookshelf = request.session.get('bookshelf', {})
        if not bookshelf:
            messages.error(request, "There's nothing in your bookshelf at the moment")
            return redirect(reverse('books'))

        current_bookshelf = bookshelf_contents(request)
        total = current_bookshelf['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

#        if request.user.is_authenticated:
#            try:
#                profile = UserProfile.objects.get(user=request.user)
#                order_form = OrderForm(initial={
#                    'full_name': profile.user.get_full_name(),
#                    'email': profile.user.email,
#                    'phone_number': profile.default_phone_number,
#                    'country': profile.default_country,
#                    'postal_code': profile.default_postal_code,
#                    'city': profile.default_city,
#                    'address_line1': profile.default_address_line1,
#                    'address_line2': profile.default_address_line2,
#                    'county': profile.default_county,
#                })
#            except UserProfile.DoesNotExist:
#                order_form = OrderForm()
#        else:
#            order_form = OrderForm()
# Instead always create new orderform

    order_form = OrderForm()


    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing.')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)

   

def checkout_success(request, order_number):
    """
    Handles successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

     # Comment out UserProfile related code
    # if request.user.is_authenticated:
    #     profile = UserProfile.objects.get(user=request.user)
    #     # Attach user profile to order
    #     order.user_profile = profile
    #     order.save()

    #     # Save the user info
    #     if save_info:
    #         profile_data = {
    #             'default_phone_number': order.phone_number,
    #             'default_country': order.country,
    #             'default_postal_code': order.postal_code,
    #             'default_city': order.city,
    #             'default_address_line1': order.address_line1,
    #             'default_address_line2': order.address_line2,
    #             'default_county': order.county,
    #         }
    #         user_profile_form = UserProfileForm(profile_data, instance=profile)
    #         if user_profile_form.is_valid():
    #             user_profile_form.save()

    messages.success(request, f'Order successfully processed \
        Order number {order_number}. Confirmation \
         will be sent to {order.email}.')

    if 'bookshelf' in request.session:
        del request.session['bookshelf']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)