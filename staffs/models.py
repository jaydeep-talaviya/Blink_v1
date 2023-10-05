from django.db import models

from products.models import Orders, Warehouse, Stocks, OrderLines
from users.models import Employee
from datetime import datetime


# Create your models here.

class OrderPrepare(models.Model):
    choices = (
        ('preparing','Preparing'),
        ('prepared','Prepared'),
    )
    order_id = models.ForeignKey(Orders,on_delete=models.DO_NOTHING)
    warehouse_id = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING)
    stock_id = models.ForeignKey(Stocks, on_delete=models.DO_NOTHING)
    purchase_qty = models.IntegerField(default=1)
    status = models.CharField(max_length=50,choices=choices)
    created_at=models.DateTimeField(auto_now_add=datetime.now)


class Ledger(models.Model):
    choices = (('order','Order'),
               ('employee_salary','Employee salary'),
               ('product_making_expense','Product Making Expense'), # to pay carpenters for product making for admin
               ('raw_material_expense','Raw Material Expense'), # to pay raw materials expense to market place
               ('other_expense','Other Expense'), # to pay amount to move one place to another place
               )
    ledger_type = models.CharField(max_length=100,choices=choices)
    creation_date = models.DateTimeField(auto_now_add=True)
    order_id = models.ForeignKey(Orders, on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self):
        return f"Ledger Entry ID: {self.id}, Type: {self.ledger_type}"

    def get_total_ledger_debit(self):
        return sum(self.ledger_line.filter(type_of_transaction='credit').values_list('amount',flat=True))

    def get_total_ledger_credit(self):
        return sum(self.ledger_line.filter(type_of_transaction='debit').values_list('amount',flat=True))

class LedgerLine(models.Model):
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE,related_name='ledger_line')
    orderline = models.ForeignKey(OrderLines, on_delete=models.DO_NOTHING,null=True,blank=True)
    type_of_transaction = models.CharField(max_length=50,choices=(('credit','CREDIT'),('debit','DEBIT')))
    transaction_date = models.DateField(auto_now=True)
    amount = models.FloatField()
    description = models.TextField(blank=True,null=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self):
        return f"Ledger Entry ID: {self.ledger.id}, Type: {self.ledger.ledger_type}, Transaction Type: {self.type_of_transaction}, Amount: {self.amount}"
