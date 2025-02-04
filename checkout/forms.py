from django import forms
from .models import Order
from django.core.validators import RegexValidator


class OrderForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+353999999999'. Up to 15 digits allowed."
    )
    phone_number = forms.CharField(validators=[phone_regex], max_length=17)

   
    eircode_regex = RegexValidator(
        regex=r'^[A-Z]\d{2}[A-Z0-9]{4}$',
        message="Please enter a valid Eircode (e.g., D02X285)"
    )
    postal_code = forms.CharField(validators=[eircode_regex], max_length=8)
    
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'address_line1', 'address_line2',
                  'city', 'postal_code', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):

        """
        Customsie form
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postal_code': 'Postal Code',
            'city': 'City',
            'address_line1': 'Address Line 1',
            'address_line2': 'Address Line 2',
            'county': 'County, State or Locality',
            'country': 'Country',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
