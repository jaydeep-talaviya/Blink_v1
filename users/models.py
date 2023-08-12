from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from datetime import date
class User(AbstractUser):
    phone_number=models.BigIntegerField(blank=True,null=True)
    profile_pic=models.ImageField(upload_to='profiles',default='default.png')
    date_of_birth=models.DateField(blank=True,null=True)
    city=models.CharField(max_length=150)

class State(models.Model):
    name = models.CharField(max_length=100)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street=models.CharField(max_length=150)
    street2=models.CharField(max_length=150,blank=True,null=True)
    city=models.CharField(max_length=150)
    state=models.ForeignKey(State, on_delete=models.PROTECT)



