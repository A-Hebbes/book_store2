from django.core.mail import send_mail
from django.conf import settings
from .models import Newsletter


def send_newsletter_email(subject, body, recipient_list=None):
    """Send newsletter email to specified recipients or all subscribers."""
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


def notify_new_book(book):
    """Send notification email about a new book to all subscribers."""
    subject = f"New Book Alert: {book.title}"
    body = (
        f"Check out our new book: '{book.title}' by {book.author}. "
        f"Available now!\n\n"
        f"Category: {book.get_category_display()}\n"
        f"Price: ${book.price}\n"
        f"Description: {book.description}\n"
    )
    send_newsletter_email(subject, body)
