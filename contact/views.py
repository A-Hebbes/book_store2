from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import ContactForm

# Create your views here.

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent. Thank you')
            return redirect(reverse('all_books'))
        else:
            messages.error(request, 'Something went wrong. Please check the form and resubmit.')
    else:
        form = ConatctForm()
    
    return render(request, 'contact/contact.html', {'form': form})