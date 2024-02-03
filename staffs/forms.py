from django import forms
from django.forms import BaseModelFormSet

from products.models import (Products, ProductChangePriceAttributes,
                             Stocks, AttributeValue, AttributeName, Vouchers, Warehouse, Delivery)
from staffs.models import Ledger, LedgerLine
from users.models import User, Employee
from django.db.models import Q

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
        exclude = ['product_maker']

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
        self.fields['expire_at'].widget = forms.TextInput(attrs={'type': 'datetime-local'})

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control formset-field'
            if self.instance.id:
                self.fields['voucher_type'].widget.attrs['readonly'] = True
                self.fields['voucher_type'].choices = list(filter(lambda x:x[0] == self.instance.voucher_type, self.fields['voucher_type'].choices))



class StocksForm(forms.ModelForm):
    class Meta:
        model=Stocks
        fields=['warehouse_id','product_id','product_attributes','total_qty','left_qty','on_alert_qty',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control formset-field'
        self.fields['warehouse_id'].widget.attrs['class'] = 'form-select formset-field'
        self.fields['warehouse_id'].widget.attrs['id'] = 'selecter_warehouse'
        self.fields['warehouse_id'].widget.attrs['onchange'] = 'handleSelectionChange()'
        self.fields['product_id'].widget.attrs['class'] = 'form-select formset-field'
        self.fields['product_id'].widget.attrs['onchange'] = 'handleSelectionChangeByProduct()'
        self.fields['warehouse_id'].label = 'Warehouse'
        self.fields['product_id'].label = 'Product'


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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        print("<<<<<<<<user\n\n\n",user.is_superuser)
        print("<<<<<<<<user\n\n\n",hasattr(user, 'employee') and user.employee.type)
        if user and user.is_authenticated:
            if user.is_superuser:
                # Add all options for admin
                self.fields['type'].widget.choices = Employee.choices
            elif hasattr(user, 'employee') and user.employee.type == 'manager':
                # Add limited options for manager
                self.fields['type'].widget.choices = Employee.manager_create_choice
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control formset-field'


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = '__all__'
        exclude = ['is_deleted','is_approved']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control formset-field'
        self.fields['owner'].widget.attrs['class'] = 'form-select formset-field'
        self.fields['address'].widget.attrs['rows'] = 1  # Set the number of rows
        instance = kwargs.get('instance', None)
        if instance and instance.pk:
            # Update mode: Only allow current owner without a warehouse
            self.fields['owner'].queryset = User.objects.filter(
                Q(employee__type='warehouse_owner') &
                Q(warehouse__isnull=True) |
                Q(pk=instance.owner.pk)  # Allow the current owner
            ).distinct()
        else:
            # Creation mode: Only allow owners without a warehouse
            self.fields['owner'].queryset = User.objects.filter(
                employee__type='warehouse_owner',
                warehouse__isnull=True
            )

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['delivery_person']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-select formset-field'
            if field == 'delivery_person':
                self.fields[field].queryset = User.objects.filter(employee__type='warehouse_owner')

class LedgerForm(forms.ModelForm):
    class Meta:
        model = Ledger
        fields = ['ledger_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-select formset-field'
        self.fields['ledger_type'].choices =  (
               ('product_making_expense','Product Making Expense'), # to pay carpenters for product making for admin
               ('raw_material_expense','Raw Material Expense'), # to pay raw materials expense to market place
               ('other_expense','Other Expense'), # to pay amount to move one place to another place
               )

class LedgerLineForm(forms.ModelForm):
    class Meta:
        model = LedgerLine
        fields = ['type_of_transaction','amount','description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-select formset-field'
        self.fields['type_of_transaction'].widget.attrs['class'] = 'form-select formset-field'
        self.fields['description'].widget.attrs['class'] = 'form-control formset-field'
        self.fields['description'].widget.attrs['rows'] = 3  # Set the number of rows

