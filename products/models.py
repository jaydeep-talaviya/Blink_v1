from django.db import models
from users.models import User,State
from django.core.validators import MaxValueValidator, MinValueValidator 
from datetime import datetime
from datetime import timedelta
from PIL import Image
from django.conf import settings

# Create your models here.
import uuid

from utils.helper_functions import get_voucher_discount


class Warehouse(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.TextField()
    created_at=models.DateTimeField()
    mobile_no=models.CharField(max_length=100)
    name=models.CharField(max_length=100)

class Category(models.Model):
    category_name=models.CharField(max_length=50)
    
    def __str__(self):
        return self.category_name

class Subcategory(models.Model):
    subcategory_name=models.CharField(max_length=50)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.subcategory_name

class AttributeName(models.Model):
    a_name=models.CharField(max_length=50)
    def __str__(self):
        return self.a_name

class AttributeValue(models.Model):
    a_value=models.CharField(max_length=50)
    a_name=models.ForeignKey(AttributeName,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.a_name.a_name +" - "+self.a_value


class Products(models.Model):
    p_name=models.CharField(max_length=50,blank=False,null=False)
    p_category=models.ForeignKey(Category, on_delete=models.CASCADE)
    p_subcategory=models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    p_created=models.DateField(auto_now_add=datetime.now)
    price=models.FloatField(validators=[MinValueValidator(1)])
    description=models.TextField()

    photo_1=models.ImageField(upload_to='products')
    photo_2=models.ImageField(upload_to='products')
    photo_3=models.ImageField(upload_to='products')
    photo_4=models.ImageField(upload_to='products',blank=True,null=True)
    photo_5=models.ImageField(upload_to='products',blank=True,null=True)
    photo_6=models.ImageField(upload_to='products',blank=True,null=True)

    def __str__(self):
        return self.p_name
    
    def save(self, *args, **kwargs):
        super(Products, self).save(*args, **kwargs)
        imag1 = Image.open(self.photo_1.path)
        if imag1.width > 400 or imag1.height> 300:
            output_size = (400, 300)
            imag1.thumbnail(output_size)
            imag1.save(self.photo_1.path)
        imag2 = Image.open(self.photo_2.path)
        if imag2.width > 400 or imag2.height> 300:
            output_size = (400, 300)
            imag2.thumbnail(output_size)
            imag2.save(self.photo_2.path)
        imag3 = Image.open(self.photo_3.path)
        if imag3.width > 400 or imag3.height> 300:
            output_size = (400, 300)
            imag3.thumbnail(output_size)
            imag3.save(self.photo_3.path)


class ProductChangePriceAttributes(models.Model):
    attribute_values=models.ManyToManyField(AttributeValue)
    p_id= models.ForeignKey(Products,on_delete=models.CASCADE)
    price=models.FloatField(validators=[MinValueValidator(1)])

    def __str__(self):
        return str(self.p_id)+" "+str(self.id)


class Rates(models.Model):
    comment=models.CharField(max_length=50)
    rate = models.PositiveIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    p_id= models.ForeignKey(Products,on_delete=models.CASCADE,blank=False,null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'p_id'], 
                name='unique product rate'
            )
        ]
    def __str__(self):
        return str(self.rate)+" by "+str(self.user)

class Stocks(models.Model):
    warehouse_id=models.ForeignKey(Warehouse,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    total_qty=models.IntegerField(validators=[MinValueValidator(1)])
    left_qty=models.IntegerField(validators=[MinValueValidator(1)])
    on_alert_qty=models.IntegerField(validators=[MinValueValidator(1)])
    finished=models.BooleanField(default=False)

class Cart(models.Model):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField(validators=[MinValueValidator(0)])
    price=models.FloatField(validators=[MinValueValidator(1)])
    selected_product_varient=models.CharField(max_length=100)
    vouchers = models.ForeignKey('Vouchers',on_delete=models.DO_NOTHING,null=True)

    def __str__(self):
        return str(self.user_id)+"'s carts "+ 'for'+ str(self.product_id.p_name)

class Checkout(models.Model):
    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    address1=models.TextField()
    address2=models.TextField(blank=True,null=True)
    state=models.ForeignKey(State,on_delete=models.SET_NULL,null=True)
    city=models.CharField(max_length=100)
    zip=models.CharField(max_length=6)
    payment_type=models.CharField(max_length=50)

    def __str__(self):
        return str(self.user)+"'s Checkout "


class Vouchers(models.Model):
    choices = (
        ('on_above_purchase', 'On Above Purchase'),
        ('deals_of_day','Deals of Day'),
        ('product_together','Product Together'),
        ('promocode','Promocode'),
    )
    voucher_type = models.CharField(max_length=200,choices=choices)
    on_above_purchase = models.FloatField(null=True,blank=True) #on_above_purchase
    off_price = models.FloatField(null=True,blank=True) #on_above_purchase + #product_together +# promocode

    products = models.ManyToManyField(Products,null=True,blank=True,related_name='products') #deals_of_day + #product_together
    percent_off = models.FloatField(null=True,blank=True) #deals_of_day

    with_product = models.ForeignKey(Products,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='with_product') #product_together

    promocode_name = models.CharField(max_length=100,null=True,blank=True) # promocode
    users=models.ManyToManyField(User,related_name='new_user_to_promo',null=True,blank=True) # promocode
    user_who_have_used=models.ManyToManyField(User,related_name='user_who_have_used',blank=True) # promocode
    created_at=models.DateTimeField(auto_now_add=datetime.now,null=True,blank=True) # promocode
    expirable=models.BooleanField(null=True,blank=True) # promocode
    expire_at=models.DateTimeField(null=True,blank=True)# promocode
    stop = models.BooleanField(null=True,blank=True,default=False) #on_above_purchase + #product_together +# promocode + #deals_of_day

class Orders(models.Model):
    
    orderstatus=[
        ('                                                                                  q','Order Not Paid'),
        ('order_confirm','Order Confirm'),
        ('order_cancel','Order Cancel'),
        ('order_delivering','Order Delivering'),
        ('order_shipped','Order Shipped'),
    ]
    orderid=models.CharField(max_length=50,default=uuid.uuid4)
    checkout=models.ForeignKey(Checkout,on_delete=models.DO_NOTHING)
    order_status=models.CharField(max_length=100,choices=orderstatus,default='order_not_confirm')
    created_at=models.DateTimeField(auto_now_add=datetime.now)
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='buyer')
    payment_failed=models.BooleanField(default=True)
    amount=models.FloatField(validators=[MinValueValidator(0)])
    total_discount=models.FloatField(validators=[MinValueValidator(0)],default=0)
    vouchers = models.ForeignKey(Vouchers,on_delete=models.DO_NOTHING,null=True)


class OrderLines(models.Model):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    qty=models.IntegerField(validators=[MinValueValidator(0)])
    unit_price=models.FloatField(validators=[MinValueValidator(1)])
    sub_total_amount=models.FloatField(validators=[MinValueValidator(0)])
    order_id=models.ForeignKey(Orders,on_delete=models.CASCADE,related_name='order')

class Delivery(models.Model):
    order = models.ForeignKey(Orders,on_delete=models.CASCADE)
    delivery_id=models.CharField(max_length=50,default=uuid.uuid4)
    state=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=datetime.now)
    delivered_at=models.DateTimeField(blank=True,null=True)

class OtpModel(models.Model):
    otp_number=models.CharField(max_length=6)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    varified=models.BooleanField(default=False)
    times=models.IntegerField(default=1)
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=datetime.now)
    payment_method=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    txnId=models.CharField(max_length=150,null=True,blank=True)
