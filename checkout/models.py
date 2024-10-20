import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from books.models import Book
from bookshop.models import Profile

class Order(models.Model):
    
    order_number = models.CharField(max_length=32, unique=True, editable=False)
    user_profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    address_line1 = models.CharField(max_length=255, null=False, blank=False)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=False, blank=False)
    county = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_cart = models.TextField(null=False, blank=False, default='')
    email_sent = models.BooleanField(default=False)

    def _generate_order_number(self):
        """
        Create order number using uuid
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        When line item is added update total including delivery
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Set an order number if not already set
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number
    
    
class OrderLineItem(models.Model):
    order = models.ForeignKey('Order', null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    book = models.ForeignKey(Book, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=1)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)   

    def save(self, *args, **kwargs):
        """
        Set lineitem total and update order total
        """
        self.lineitem_total = self.book.price * self.quantity
        super().save(*args, **kwargs)
        self.order.update_total()

    def __str__(self):
        return f'{self.quantity} x "{self.book.title}" on order {self.order.order_number}'