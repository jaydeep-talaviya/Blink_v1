from django.forms import BaseModelFormSet

from .models import Rates, Checkout, Category, Subcategory
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


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category_name'].widget.attrs['class'] = 'form-control formset-field'
        self.fields['category_name'].required = True

class CategoryFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()
        # For example, check some condition across all forms
        for form in self.forms:
            if not form.cleaned_data.get('category_name'):
                raise forms.ValidationError("Category Name should be provided")


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory_name'].widget.attrs['class'] = 'form-control formset-field'
        self.fields['subcategory_name'].required = True
        self.fields['category'].widget.attrs['class'] = 'form-control formset-field'
        self.fields['category'].required = True

class SubCategoryFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()
        # For example, check some condition across all forms
        for form in self.forms:
            if not form.cleaned_data.get('subcategory_name'):
                raise forms.ValidationError("Sub-Category Name should be provided")
            if not form.cleaned_data.get('category'):
                raise forms.ValidationError("Category should be provided")
