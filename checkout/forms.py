from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
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