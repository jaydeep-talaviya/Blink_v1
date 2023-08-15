from django.urls import path,include
from .views import (home,registration,loginpage,logoutuser,change_password,profilesave,profileshow,profile_delete)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',home,name='home'),
    path('registration',registration,name='registration'),
    path('login/',loginpage,name='login'),
    path('logout',logoutuser,name='logout'),
    
    path('profile/update',profilesave,name='profilesave'),
    path('profileshow',profileshow,name='profileshow'),
    path('profile/delete/<int:id>',profile_delete,name='profile_delete'),

    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='passwordreset/password_reset.html',subject_template_name='passwordreset/password_reset_subject.txt',email_template_name='passwordreset/password_reset_email.html',),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='passwordreset/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='passwordreset/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='passwordreset/password_reset_complete.html'),name='password_reset_complete'),

    path('password-change',change_password, name='change_password'),

    # path('accounts/social/login/cancelled/',loginpage,name='cancled_login'),
    # path('accounts/social/signup/',google_form,name='Signup')
]