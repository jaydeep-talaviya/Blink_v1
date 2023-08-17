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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['p_name'].widget.attrs['class'] = 'form-control formset-field'
        self.fields['p_category'].widget.attrs['class'] = 'form-control formset-field'
        self.fields['p_subcategory'].widget.attrs['class'] = 'form-control formset-field'
        self.fields['price'].widget.attrs['class'] = 'form-control formset-field'
        self.fields['description'].widget.attrs['class'] = 'form-control formset-field'
        self.fields['description'].widget.attrs['rows'] = 3  # Set the number of rows

class ProductChangePriceAttributesForm(forms.ModelForm):
    a_name = forms.ModelChoiceField(required=True,queryset=AttributeName.objects.all())
    a_value = forms.ModelChoiceField(required=True,queryset=AttributeValue.objects.none())

    class Meta:
        model=ProductChangePriceAttributes
        fields=['a_name','a_value','price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['a_name'].widget.attrs['class'] = 'form-control formset-field'
        self.fields['a_value'].widget.attrs['class'] = 'form-control formset-field'
        self.fields['price'].widget.attrs['class'] = 'form-control formset-field'


ProductChangePriceAttributesFormSet = forms.inlineformset_factory(
    Products,
    ProductChangePriceAttributes,
    form=ProductChangePriceAttributesForm,
    extra=1,  # Number of empty forms to display initially
    can_delete=True,
)

class StocksForm(forms.ModelForm):
    class Meta:
        model=Stocks
        fields=['left_qty','total_qty','on_alert_qty','product_id']

