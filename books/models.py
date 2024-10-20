from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from newsletter.utils import notify_new_book


BOOK_CATEGORIES = [
    ('classics', 'Classics'),
    ('historical', 'Historical'),
    ('mystery_thriller', 'Mystery & Thriller'),
    ('scifi_fantasy', 'Science Fiction & Fantasy'),
    ('biography', 'Biography & Memoir'),
    ('other', 'Other'),
]


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.CharField(max_length=255)
    isbn = models.CharField(
        max_length=13,
        unique=True,
        help_text="13 Character ISBN number"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=100,
        choices=BOOK_CATEGORIES,
        default='other'
    )
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='books/', null=True, blank=True)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Book)
def book_created(sender, instance, created, **kwargs):
    if created:
        notify_new_book(instance)
