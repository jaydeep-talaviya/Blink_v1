from django.db.models import Q
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from notifications_app.models import Notification
from staffs.models import LedgerLine, Ledger
from users.models import User, Employee
from utils.helper_functions import get_voucher_discount, get_related_url
from .models import OtpModel, Orders, OrderLines, Cart, Products, Stocks, Payment, Delivery, Vouchers
from datetime import datetime
from datetime import date
import requests
import json
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

MERCHANT_KEY = 'Z9uzcquqrxUuNErK'

# import checksum generation utility
from paytmchecksum import PaytmChecksum
from staffs.middleware import get_current_user, get_request

today = date.today()

@receiver(post_save, sender=OtpModel) 
def create_otp(sender, instance, created, **kwargs):
    if instance.verified == True:
        cart=Cart.objects.filter(user_id=instance.user)
        checkout=instance.user.checkout_set.last()
        if len(cart)!=0 and checkout.payment_type == 'case_on_delivery':
            orders=Orders.objects.create(checkout=checkout,order_status='order_confirm',user=instance.user,amount=0,vouchers=cart.last().vouchers if cart.last().vouchers else None)
            amount=0
            for c in cart:
                OrderLines.objects.create(product_id=c.product_id,qty=c.qty,unit_price=c.price,sub_total_amount=c.qty*c.price,order_id=orders,selected_product_varient=c.selected_product_varient)
                amount+=c.qty*c.price

            voucher=cart.last().vouchers
            discount_amount = 0
            try:
                discount_amount = get_voucher_discount(voucher, instance.user, amount)
            except Exception:
                print('>> something went wrong')
            amount=amount-discount_amount
            Payment.objects.create(user=orders.user,order_id=orders,payment_method='Offline',status='Pending')
            orders.amount=amount
            orders.total_discount = discount_amount
            orders.payment_failed=False
            orders.save()
            cart.delete() 
            instance.times=0

            managers = Employee.objects.filter(Q(type='manager')).values('user')
            request = get_request()
            related_url = get_related_url(request, 'order')

            # notify to each manager.
            for manager in managers:
                Notification.objects.create(sender=request.user, receiver_id=manager.get('user'),
                                            message='New Order has been Updated, Please check!',
                                            related_url=related_url
                                            )


# @receiver(post_save, sender=Payment)
# def create_delivery_on_payment_success(sender, instance, created, **kwargs):
#     if instance.status!='Failed' and created:
#         delivery=Delivery.objects.create(order=instance.order_id,state='Confirm')
#         delivery.save()


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
            payment.status = 'Success'
            payment.save()
        create_ledger = Ledger(ledger_type='order', order_id_id=instance.order.id)
        create_ledger.save()
        for orderline in instance.order.order.all():
            LedgerLine.objects.create(ledger_id=create_ledger.id, orderline_id=orderline.id, type_of_transaction='credit',
                                      amount=orderline.sub_total_amount,
                                      description=f'Transaction Credited for Order ID:{orderline.order_id.orderid} for Product {orderline.product_id}')
        if instance.order.vouchers:
            discount_amount = sum([i.sub_total_amount for i in instance.order.order.all()]) - instance.order.amount

            if discount_amount:
                LedgerLine.objects.create(ledger_id=create_ledger.id,
                                          type_of_transaction='debit',
                                          amount=discount_amount,
                                          description=f'Transaction Debited for Order ID:{instance.order.orderid} for Voucher Discount {instance.order.vouchers}')


@receiver(post_save, sender=Orders)
def on_cancel_order_remove_delivery(sender, instance, created, **kwargs):
    admin = User.objects.filter(is_superuser=True).first()

    if instance.order_status == 'order_confirm':
        if instance.vouchers:
            voucher = instance.vouchers
            if voucher.voucher_type == 'promocode':
                voucher.user_who_have_used.add(instance.user)
        # notification to admin for create prepare order
        # Notification.objects.create(buyer=instance.user,seller=admin, user_order=instance,
        #                             message='Prepare Order for Order Id: ' + str(instance.orderid),
        #                             for_admin=True)

    if instance.order_status == 'order_cancel':
        if instance.payment_set.all():
            instance.delivery_set.all().delete()
            payment=instance.payment_set.last()
            payment.status='Cancel'
            payment.save()
        if instance.vouchers:
            voucher = instance.vouchers
            if voucher.voucher_type == 'promocode':
                voucher.user_who_have_used.remove(instance.user)
        # Notification.objects.create(buyer=instance.user, seller=admin, user_order=instance,
        #                             message='Order cancelled for Order Id: ' + str(instance.orderid),
        #                             for_admin=True)

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


@receiver(post_save, sender=Stocks)
def check_finished_or_not(sender, instance, created, **kwargs):
    if instance.left_qty == 0:
        instance.finished = True
        instance.save()
        managers = Employee.objects.filter(type='manager').values('user')
        current_user = get_current_user()
        # notify to each manager.
        for manager in managers:
            Notification.objects.create(sender=current_user, receiver_id=manager.get('user'),
                                        message='Stock has been updated!',
                                        related_url=current_user
                                        )