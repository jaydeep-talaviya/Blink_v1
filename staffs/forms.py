from django import forms
from django.forms import BaseModelFormSet

from products.models import (Products, ProductChangePriceAttributes,
                             Stocks, AttributeValue, AttributeName)

########## Attribute Name ###########33
class AttributeNameForm(forms.ModelForm):
    class Meta:
        model = AttributeName
        fields='__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['a_name'].widget.attrs['class'] = 'form-control formset-field'
        self.fields['a_name'].required = True

class AttributeNameFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()
        # For example, check some condition across all forms
        for form in self.forms:
            if not form.cleaned_data.get('a_name'):
                raise forms.ValidationError("Attribute Name should be atleast one character")


######## attribute Value #################

class ProductAttributesForm(forms.ModelForm):
    class Meta:
        model=AttributeValue
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['a_name'].widget.attrs['class'] = 'form-control formset-field'
        self.fields['a_value'].widget.attrs['class'] = 'form-control formset-field'

class AttributeValueFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()
        # For example, check some condition across all forms
        for form in self.forms:
            if not form.cleaned_data.get('a_name'):
                raise forms.ValidationError("Please Select Attribute Name ")
            if not form.cleaned_data.get('a_value'):
                raise forms.ValidationError("Attribute Value should be atleast one character")




class ProductForm(forms.ModelForm):
    class Meta:
        model=Products
        fields='__all__'

class ProductChangePriceAttributesForm(forms.ModelForm):
    class Meta:
        model=ProductChangePriceAttributes
        fields=['attribute_values','price']

class StocksForm(forms.ModelForm):
    class Meta:
        model=Stocks
        fields=['left_qty','total_qty','on_alert_qty','product_id']

