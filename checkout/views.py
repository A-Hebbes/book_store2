from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from books.models import Book
from bookshelf.contexts import bookshelf_contents
from .utils import send_confirmation_email

import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(
            pid,
            metadata={
                'bookshelf': json.dumps(request.session.get('bookshelf', {})),
                'save_info': request.POST.get('save_info'),
                'username': request.user.username if request.user.is_authenticated  # noqa: E501
                else 'AnonymousUser',
            }
        )
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            'Sorry, your payment cannot be processed right now. '
            'Please try again later.'
        )
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
                    book = Book.objects.get(book_id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            book=book,
                            quantity=item_data,
                        )
                        order_line_item.save()
                except Book.DoesNotExist:
                    messages.error(
                        request,
                        "One of the books in your bookshelf wasn't found. "
                        "Please call us for assistance!"
                    )
                    order.delete()
                    return redirect(reverse('view_bookshelf'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(
                reverse('checkout_success', args=[order.order_number])
            )
        else:
            for field, errors in order_form.errors.items():
                for error in errors:
                    messages.error(
                        request,
                        f"{order_form.fields[field].label}: {error}"
                    )
            return redirect(reverse('checkout'))

    else:
        bookshelf = request.session.get('bookshelf', {})
        if not bookshelf:
            messages.error(
                request,
                "There's nothing in your bookshelf at the moment"
            )
            return redirect(reverse('books'))

        current_bookshelf = bookshelf_contents(request)
        total = current_bookshelf['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        try:
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )
        except stripe.error.StripeError as e:
            messages.error(
                request,
                f"An error occurred while processing your payment: {str(e)}"
            )
            return redirect(reverse('view_bookshelf'))

    order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(
            request,
            'Stripe public key is missing. '
            'Did you forget to set it in your environment?'
        )

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """Handle successful checkouts"""
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if not order.email_sent:
        email_sent = send_confirmation_email(order)

        if email_sent:
            order.email_sent = True
            order.save()
            messages.success(
                request,
                f'Order successfully processed! Your order number is '
                f'{order_number}. A confirmation email has been sent to '
                f'{order.email}.'
            )
        else:
            messages.warning(
                request,
                f'Order processed, but we couldn\'t send a confirmation email '
                f'to {order.email}. Please contact us if you don\'t receive '
                f'it shortly.'
            )
    else:
        messages.info(
            request,
            f'A confirmation email for order {order_number} has already been '
            f'sent to {order.email}.'
        )

    if 'bookshelf' in request.session:
        del request.session['bookshelf']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
