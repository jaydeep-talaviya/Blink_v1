from django import forms
from products.models import (Products,ProductChangePriceAttributes,
                            Stocks,AttributeValue,Deals_of_day)

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

class StocksForm(forms.ModelForm):
    class Meta:
        model=Stocks
        fields=['left_qty','total_qty','on_alert_qty','product_id']

class Deals_of_dayForm(forms.ModelForm):
    date = forms.DateField(
    widget=forms.TextInput(     
        attrs={'type': 'date'} 
    )
)                                           
    class Meta:
        model=Deals_of_day
        fields='__all__'