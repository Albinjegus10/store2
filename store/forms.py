from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ContactMessage
class SignupForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    image = forms.ImageField(required=False)
    address = forms.CharField(max_length=255, required=False)

    # Remove help text for all fields
    username = forms.CharField(max_length=30, required=True, help_text='')
    password1 = forms.CharField(label='Password', strip=False, help_text='', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', strip=False, help_text='', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'name', 'phone_number', 'image', 'address']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = '__all__'


from django import forms
from .models import Billing

class YourBillingForm(forms.ModelForm):
    PAYMENT_METHOD_CHOICES = [
        ('paypal', 'Paypal'),
        ('Gpay', 'Google Pay'),
        ('phonepe', 'PhonePe'),
        ('cashdelivery', 'Cash On Delivery'),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect,
        initial='paypal',  # You can set the default selected payment method
    )
    class Meta:
        model = Billing
        fields = '__all__'

from django import forms
class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    # You can include other fields if needed
from .models import Order_details
class OrderDetailsForm(forms.ModelForm):
    class Meta:
        model = Order_details
        exclude = ['product_id', 'user_id', 'order_date', 'status']

    def __init__(self, *args, **kwargs):
        super(OrderDetailsForm, self).__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super(OrderDetailsForm, self).clean()

        # Example: Check if required fields are not empty
        required_fields = ['first_name', 'last_name', 'country', 'state', 'town_city', 'street_address', 'postcode',
                           'phone', 'email', 'payment_method']
        for field_name in required_fields:
            if not cleaned_data.get(field_name):
                self.add_error(field_name, f'The {field_name} field is required.')

        return cleaned_data
from django import forms


from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'phone_number', 'image', 'address']

class PriceFilterForm(forms.Form):
    minamount = forms.DecimalField(required=False, min_value=0, max_digits=10, decimal_places=2)
    maxamount = forms.DecimalField(required=False, min_value=0, max_digits=10, decimal_places=2)

    def clean(self):
        cleaned_data = super().clean()
        minamount = cleaned_data.get('minamount')
        maxamount = cleaned_data.get('maxamount')
        if minamount is not None and maxamount is not None and minamount > maxamount:
            raise forms.ValidationError('Min amount must be less than or equal to max amount.')
        return cleaned_data

from .models import ContactMessage,Checkout,Reason


class ReturnForm(forms.ModelForm):
    class Meta:
        model = Reason
        fields = ['Return_Reason']
class CancelForm(forms.ModelForm):
    class Meta:
        model = Reason
        fields = ['cancellation_reason']