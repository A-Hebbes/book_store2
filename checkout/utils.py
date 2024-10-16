from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from books.models import Book

import logging

logger = logging.getLogger(__name__)

def send_confirmation_email(order):
    """Send the user a confirmation email"""
    try:
        logger.info(f"Attempting to send confirmation email for order {order.id}")
        
        cust_email = order.email
        logger.info(f"Customer email: {cust_email}")
        
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        logger.info("Email subject rendered")
        
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        logger.info("Email body rendered")
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )
        logger.info("Email sent successfully")
        
        return True
    except Exception as e:
        logger.error(f"Failed to send confirmation email: {str(e)}")
        return False