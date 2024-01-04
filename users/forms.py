from django import forms

from utils.helper_functions import send_email_with_template
from .models import User, EmployeeSalary
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q


class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=100,widget=forms.PasswordInput)
    password = forms.CharField(max_length=100,widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','phone_number','password','confirm_password']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        print(">>>comming 3",cleaned_data)

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data

    def save(self, commit=True):
        print(">>>comming 2")

        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        send_email_with_template(self.cleaned_data['username'],self.cleaned_data['email'])
        return user


class UserLoginForm(forms.Form):
    usernameoremail=forms.CharField(error_messages={'required':"please Enter Username"})
    password=forms.CharField(widget=forms.PasswordInput,error_messages={'required':"Please Enter Password"})
    

class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','profile_pic','phone_number','date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

class EmployeeSalaryForm(forms.ModelForm):
    class Meta:
        model = EmployeeSalary
        fields = ['salary']


    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-select formset-field'
        self.fields['salary'].widget.attrs['min'] = 1
        self.fields['salary'].widget.attrs['step'] = 0.1

