from django import forms
from .models import User

class UserRegistrationForm(forms.Form):
    username=forms.CharField(error_messages={'required':"please Enter Username"})
    email=forms.EmailField(error_messages={'required':"Please Enter Correct Email Address"})
    password=forms.CharField(widget=forms.PasswordInput,error_messages={'required':"Please Enter Password"})
    password2=forms.CharField(error_messages={'required':"Please Enter Correct Password"},label="Confirm Password",widget=forms.PasswordInput)
    



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