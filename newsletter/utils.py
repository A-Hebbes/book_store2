from django.core.mail import send_mail
from django.conf import settings
from .models import Newsletter

def send_newsletter_email(subject, body, recipient_list=None):
    if recipient_list is None:
        # Get all subscribed emails
        recipient_list = Newsletter.objects.values_list('email', flat=True)
    
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )

# Function to notify about new books
def notify_new_book(book):
    subject = f"New Book Alert: {book.title}"
    body = f"Check out our new book: '{book.title}' by {book.author}. Available now!\n\n"
    body += f"Category: {book.get_category_display()}\n"
    body += f"Price: ${book.price}\n"
    body += f"Description: {book.description}\n"
    send_newsletter_email(subject, body)