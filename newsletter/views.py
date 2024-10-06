from django.shortcuts import render, redirect
from .forms import NewsletterForm

# Create your views here.

def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully subscribed')
            return redirect(reverse('all_books'))  
    else:
        form = NewsletterForm()
        messages.error(request, 'Something went wrong. Check the form and resubmit')
        return render(request, 'newsletter/signup.html', {'form': form})