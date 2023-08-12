from .models import Rates,Checkout
from django import forms

class RatesForm(forms.ModelForm):

    class Meta:
        model = Rates
        fields = ("__all__")


class CheckoutForm(forms.ModelForm):
    payment=[
        ('case_on_delivery','Case On Delivery'),
        ('paytm',"Using Paytm"),
        ('paypal','Using Paypal'),
        ('debit_credit','Using Debit/Credit Card')
    ]
    payment_type = forms.ChoiceField(choices=payment, widget=forms.RadioSelect())

    class Meta:
        model = Checkout
        exclude = ('user',)


# class ReturnProductForm(forms.ModelForm):

#     class Meta:
#         model = Return_product
#         exclude = ('order','user')
