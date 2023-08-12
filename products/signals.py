from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from users.models import User
from .models import OtpModel,Orders,OrderLines,Cart,Products,Stocks,Discount,Payment,Delivery
from datetime import datetime
from datetime import date
import requests
import json
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

MERCHANT_KEY = 'Z9uzcquqrxUuNErK'

# import checksum generation utility
# You can get this utility from https://developer.paytm.com/docs/checksum/
from paytmchecksum import PaytmChecksum

today = date.today()


@receiver(post_save, sender=OtpModel) 
def create_otp(sender, instance, created, **kwargs):
    if instance.varified == True:
        cart=Cart.objects.filter(user_id=instance.user)
        checkout=instance.user.checkout_set.get()
        if len(cart)!=0:
            seller=User.objects.get(order_place_city=instance.user.order_place_city,is_staff=True)
            orders=Orders.objects.create(checkout=checkout,order_status='order_confirm',user=instance.user,amount=0,created_seller=seller)
            amount=0
            for c in cart:
                if checkout.payment_type == 'case_on_delivery':
                    OrderLines.objects.create(product_id=c.product_id,qty=c.qty,price=c.price,per_order_amount=c.qty*c.price,order_id=orders)
                    amount+=c.qty*c.price
                stock=c.product_id.stocks_set.filter(stock_day__day=today.day,stock_day__month=today.month,stock_day__year=today.year,left_qty__gt=0)[0]
                stock.left_qty=stock.left_qty-c.qty
                stock.save()
            discount=Discount.objects.filter(on_above_purchase__lte=amount)
            if discount:
                discount=discount.last()
                orders.discount=discount
                amount-=(amount*discount.percent_off)/100
            Payment.objects.create(user=orders.user,order_id=orders,payment_method='Offline',status='Pending')
            orders.amount=amount
            orders.payment_failed=False
            orders.save()
            cart.delete() 
            instance.times=0
            # Profile.objects.create(user=instance)
 


@receiver(post_save, sender=Payment) 
def create_delivery_on_payment_success(sender, instance, created, **kwargs):
    if instance.status!='Failed' and created:
        delivery=Delivery.objects.create(order=instance.order_id,state='Confirm')
        delivery.save()


@receiver(post_save, sender=Delivery)
def change_order_status(sender, instance, created, **kwargs):
    if instance.state=='Delivering':
        instance.order.order_status='order_delivering'
        instance.order.save()
    if instance.state=='Shipped':
        instance.order.order_status='order_shipped'
        instance.order.save()
        if instance.order.payment_set.last().status == 'Pending':
            payment=instance.order.payment_set.last()
            payment.status = 'SUCCESS'
            payment.save()


@receiver(post_save, sender=Orders)
def on_cancel_order_remove_delivery(sender, instance, created, **kwargs):

    if instance.order_status == 'order_cancel':
        orderlines=instance.order.all()

        for orderline in orderlines:
            last_stock=orderline.product_id.stocks_set.last()
            last_stock.left_qty+=orderline.qty
            last_stock.save()
        if instance.payment_set.all():
            instance.delivery_set.all().delete()
            payment=instance.payment_set.last()
            payment.status='Cancel'
            payment.save()


@receiver(post_save, sender=Payment)
def on_payment_cancel(sender, instance, created, **kwargs):
    if instance.status=='Cancel' and instance.payment_method == 'Online':
        paytmParams = dict()
        refund_amount=instance.order_id.amount-((instance.order_id.amount*10)/100)
        if refund_amount > 0:
            paytmParams["body"]= {
                "mid"          : "iNqaaK84118094196288",
                "txnType"      : "REFUND",
                "orderId"      : str(instance.order_id.orderid),
                "txnId"        : str(instance.txnId),
                "refId"        : str(instance.order_id.orderid)+"abcz",
                "refundAmount" : str(refund_amount),
            }
            checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), MERCHANT_KEY)
            paytmParams["head"] = {
                "signature"    : checksum
            }
            post_data = json.dumps(paytmParams)
            # for Staging
            url = "https://securegw-stage.paytm.in/refund/apply"
            response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
            print(response)
            try:
                if response['body']['resultInfo']['resultCode'] ==  '601':
                    subject = f" Refund of Your Order "
                    message = f"""
                    Dear Customer {instance.order_id.user.username}, 
                    Your Order {response['body']['orderId']} has been cancel. 
                    Refund amount will be 10% less then origional order amount.
                    Shortly Your refund amount {response['body']['refundAmount']} will be transfer to you.
                    Thanks!.
                    
                    
                    Note: it may take 2-3 days to get refund due to bank policy.
                    """
                    
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [instance.order_id.user.email, ]
                    send_mail( subject, message, email_from, recipient_list )
            except Exception as e:
                print(e)