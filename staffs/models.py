from django.db import models

from products.models import Orders, Warehouse, Stocks


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

