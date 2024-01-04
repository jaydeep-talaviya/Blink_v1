from django.shortcuts import render,redirect

from utils.helper_functions import send_email_with_template
from .models import User
from . forms import UserRegistrationForm,UserLoginForm,UpdateForm
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'users/home.html')

def registration(request):
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            print(">>>comming 1")
            form.save()
            messages.success(request, "User Created Successfully! please Login")
            return redirect('login')
        else:
            messages.warning(request, "Please Enter Validate Credentials")
            form=UserRegistrationForm()
            return render(request,'users/register.html',{'form':form})
    form=UserRegistrationForm()
    return render(request,'users/register.html',{'form':form})


def loginpage(request):
    if request.method == 'POST':
        next_url = request.GET.get("next", None)
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('usernameoremail')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(request, username=username_or_email, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'You are now logged in')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def logoutuser(request):
    auth.logout(request)
    messages.warning(request, 'You Are Logged Out Successfully')
    return redirect('home')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'passwordreset/change_password.html', {
        'form': form
    })

@login_required
def profilesave(request):
    if request.method=="POST":
        form2=UpdateForm(request.POST or None,request.FILES or None,instance=request.user)
        if form2.is_valid():
            form2.save()
            if form2.has_changed()==True:
                messages.success(request, 'successfully Updated profile')
            else:
                 messages.success(request, "You have not changed anything!")
            return redirect('profileshow')
        else:
            messages.error(request, 'sorry! there is error something! Try Again')
            return render(request,'users/profile.html',{"form2":form2})
    else:
        form2 = UpdateForm(instance=request.user)
        return render(request, 'users/profile.html', {"form2": form2})

def profileshow(request):
    form2 = UpdateForm(instance=request.user)
    return render(request, 'users/profile.html',{"form2":form2,'disabled':'disabled'})

def profile_delete(request,id):
    exist_user = User.objects.filter(id=id)
    exist_user.delete()
    return redirect('logout')

##### Extra Pages
def bad_request(request,exception):
    return render(request,'global/page_400.html',{})

def permission_denied(request, exception=None):
    return render(request,'global/page_403.html',{})

def page_not_found(request,exception):
    return render(request,'global/page_404.html',{})

def server_error(request,exception=None):
    return render(request,'global/page_500.html',{})