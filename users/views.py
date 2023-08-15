from django.shortcuts import render,redirect

from utils.helper_functions import send_email_with_template
from .models import User
from . forms import UserRegistrationForm,UserLoginForm,UpdateForm
from django.contrib import auth
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
# from products.models import DealsViaCard
# from django.contrib.auth.models import User as AllUser
from django.contrib.auth.decorators import login_required
from products.models import Store

# Create your views here.
def home(request):
    return render(request,'users/home.html')


def registration(request):
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            password2=form.cleaned_data.get('password2')
            existusername=User.objects.all().filter(username=username)
            if len(existusername) == 0:
                if password2==password:
                    user=User.objects.create(username=username,email=email,password=password2)
                    user.set_password(password2)
                    user.save()
                    send_email_with_template(username, email)
                    messages.success(request, "User Created Successfully! please Login")
                    return redirect('login')
                else:
                    messages.warning(request, "Password Doesn't Match! Try Again")
                    form=UserRegistrationForm()
                    return render(request,'users/register.html',{'form':form})
            else:
                messages.warning(request, "Username Already Exist! Please Enter Valid Username!")
                form=UserRegistrationForm()
                return render(request,'users/register.html',{'form':form})
        else:
            messages.warning(request, "Please Enter Validate Credentials")
            form=UserRegistrationForm()
            return render(request,'users/register.html',{'form':form})
    form=UserRegistrationForm()
    return render(request,'users/register.html',{'form':form})


def loginpage(request):
    if request.method == 'POST':
        next_url=request.GET.get("next", None)
        form=UserLoginForm(request.POST)
        if form.is_valid():
            username_or_email=form.cleaned_data.get('usernameoremail')
            password=form.cleaned_data.get('password')
            username=User.objects.filter(Q(username=username_or_email) | Q(email=username_or_email))
            user = None
            if len(username)!=0 and len(username)==1:
                username=username[0].username
                user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'You are now logged in')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
                form=UserLoginForm()
                return render(request,'users/login.html',{'form':form})
    form=UserLoginForm()
    return render(request,'users/login.html',{'form':form})

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
                 messages.success(request, "You have not Changed anything!")
            return redirect('profileshow')
        else:
            messages.error(request, 'sorry! there is error something! Try Again')
            return render(request,'users/profile.html',{"form2":form2})
    else:

        form2 = UpdateForm(instance=request.user)

        # messages.info(request,"update Your profile!")
        return render(request, 'users/profile.html', {"form2": form2})
    return render(request, 'users/profile.html', {"form2": form2})

def profileshow(request):
    form2 = UpdateForm(instance=request.user)
    return render(request, 'users/profile.html',{"form2":form2,'disabled':'disabled'})

def profile_delete(request,id):
    exist_user = User.objects.filter(id=id)
    exist_user.delete()
    return redirect('logout')