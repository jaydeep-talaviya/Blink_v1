from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
# Create your models here.
from datetime import date


class CustomUserManager(UserManager):
    def get_admin(self):
        return self.filter(is_superuser=True).first()

class User(AbstractUser):
    phone_number=models.BigIntegerField(blank=True,null=True)
    profile_pic=models.ImageField(upload_to='profiles',default='default.png')
    date_of_birth=models.DateField(blank=True,null=True)
    city=models.CharField(max_length=150)
    objects = CustomUserManager()

class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street=models.CharField(max_length=150)
    street2=models.CharField(max_length=150,blank=True,null=True)
    city=models.CharField(max_length=150)
    state=models.ForeignKey(State, on_delete=models.PROTECT)

class Employee(models.Model):
    manager_create_choice = [
        ('warehouse_owner', 'Warehouse Owner'),
        ('delivery_person', 'Delivery Person'),
        ('product_maker', 'Product Maker'),
        ('qa', 'QA'),
        ('other', 'Other'),
    ]
    choices = [
        ('manager','Manager')
    ] + manager_create_choice
    type = models.CharField(max_length=255,choices=choices)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    salary = models.FloatField(default=0,null=True,blank=True)

    def __str__(self):
        return self.user.username


class EmployeeSalary(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    salary = models.FloatField(default=0)
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.employee.user.username+"s' Salary" + str(self.salary)