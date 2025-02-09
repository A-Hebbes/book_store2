from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import NewsletterForm


def newsletter_signup(request):
    """Handle newsletter signup form submission."""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully subscribed')
            return redirect(reverse('all_books'))
        else:
            messages.error(
                request,
                'We already have that email registered, '
                'please use a different email'
            )
    else:
        form = NewsletterForm()
    return render(request, 'newsletter/signup.html', {'form': form})
