from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from notifications_app.models import Notification
from staffs.models import OrderPrepare, Ledger, LedgerLine
from users.models import EmployeeSalary, User


@receiver(post_save, sender=OrderPrepare)
def create_ledger_for_order(sender, instance, created, **kwargs):
    if created:
        create_ledger = Ledger(ledger_type='order',order_id_id=instance.order_id.id)
        create_ledger.save()
        if instance.order_id.payment_set.last().payment_method == 'Online':
            for orderline in instance.order_id.order.all():
                LedgerLine.objects.create(ledger_id=create_ledger.id, orderline_id=orderline.id, type_of_transaction='credit',
                                          amount=orderline.sub_total_amount,
                                          description=f'Transaction Credited for Order ID:{orderline.order_id.orderid} for Product {orderline.product_id}')
            if instance.order_id.vouchers:
                discount_amount = sum([i.sub_total_amount for i in instance.order_id.order.all()]) - instance.order_id.amount

                if discount_amount:
                    LedgerLine.objects.create(ledger_id=create_ledger.id,
                                              type_of_transaction='debit',
                                              amount=discount_amount,
                                              description=f'Transaction Debited for Order ID:{instance.order_id.orderid} for Voucher Discount {instance.order_id.get_name()}')
            #send notification to his/her self to create delivery
            admin = User.objects.filter(is_superuser=True).first()
            # Notification.objects.create(seller=admin,user_order=instance.order_id,prepare_order=instance,message='Create Delivery for Order Id: '+ str(instance.order_id.orderid),for_admin=True)



@receiver(post_save, sender=EmployeeSalary)
def create_ledger_for_employee_salary(sender, instance, created, **kwargs):
    if created:
        create_ledger = Ledger(ledger_type='employee_salary')
        create_ledger.save()
        LedgerLine.objects.create(ledger_id=create_ledger.id, employee_id_id=instance.employee.id, type_of_transaction='debit',
                                      amount=instance.salary,
                                      description=f'Transaction Debited for Salary :{instance.salary} Rs. and credited to {instance.employee.user.username}')
