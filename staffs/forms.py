from django import forms
from products.models import (Products, ProductChangePriceAttributes,
                             Stocks, AttributeValue, AttributeName)


class AttributeNameForm(forms.ModelForm):
    class Meta:
        model = AttributeName
        fields='__all__'
        widgets = {
            'a_name': forms.TextInput(attrs={'class': 'form-control formset-field'})
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model=Products
        fields='__all__'

class ProductChangePriceAttributesForm(forms.ModelForm):
    class Meta:
        model=ProductChangePriceAttributes
        fields=['attribute_values','price']

class ProductAttributesForm(forms.ModelForm):
    class Meta:
        model=AttributeValue
        fields='__all__'
        widgets = {
            'a_name': forms.Select(attrs={'class': 'form-control formset-field'}),
            'a_value': forms.TextInput(attrs={'class': 'form-control formset-field'})

        }


class StocksForm(forms.ModelForm):
    class Meta:
        model=Stocks
        fields=['left_qty','total_qty','on_alert_qty','product_id']

