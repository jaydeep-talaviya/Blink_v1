from django import forms
from django.forms import BaseModelFormSet

from products.models import (Products, ProductChangePriceAttributes,
                             Stocks, AttributeValue, AttributeName, Vouchers,Warehouse)
from users.models import User, Employee


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
        if self.instance.id:
            self.fields['p_name'].initial = self.instance.p_name
            self.fields['p_category'].initial = self.instance.p_category
            self.fields['p_subcategory'].initial = self.instance.p_subcategory
            self.fields['price'].initial = self.instance.price
            self.fields['description'].initial = self.instance.description

class ProductChangePriceAttributesForm(forms.ModelForm):

    class Meta:
        model=ProductChangePriceAttributes
        fields=['attribute_values','price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['attribute_values'].widget.attrs['class'] = 'form-select formset-field'
        self.fields['price'].widget.attrs['class'] = 'form-control formset-field'

    def clean(self):
        cleaned_data = super().clean()
        # Print cleaned_data or specific field values for debugging
        print(cleaned_data,">>>>>>>>\n\n\n\n\n")
        return cleaned_data


ProductChangePriceAttributesFormSet = forms.inlineformset_factory(
    Products,
    ProductChangePriceAttributes,
    form=ProductChangePriceAttributesForm,
    extra=1,  # Number of empty forms to display initially
    can_delete=True,
)

class VouchersForm(forms.ModelForm):
    class Meta:
        model=Vouchers
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-select formset-field'


class StocksForm(forms.ModelForm):
    class Meta:
        model=Stocks
        fields=['left_qty','total_qty','on_alert_qty','product_id']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control formset-field'

class EmployeeForm(forms.ModelForm):
    type = forms.ChoiceField(choices=Employee.choices)
    class Meta:
        model = Employee
        fields = ['type','salary']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control formset-field'

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control formset-field'
        self.fields['owner'].widget.attrs['class'] = 'form-select formset-field'
        self.fields['address'].widget.attrs['rows'] = 1  # Set the number of rows
        self.fields['owner'].queryset = User.objects.filter(employee__type='warehouse_owner')
