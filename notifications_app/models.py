from django.db import models
from django.db.models.signals import post_save
from products.models import Delivery
from users.models import User
from django.dispatch import receiver
from django_celery_beat.models import MINUTES, PeriodicTask, CrontabSchedule, PeriodicTasks
import json

# Create your models here.
class Notification(models.Model):
    buyer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_buyer')
    seller=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_seller')
    delivery=models.ForeignKey(Delivery,on_delete=models.CASCADE)
    message=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now=True)
    sent=models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']


@receiver(post_save,sender=Delivery)
def create_notification(sender,instance,created,update_fields,**kwargs):
    #call group_send function directly to send notifications or you can create a dynamic task in celery beat
    admin = User.objects.filter(is_superuser=True).first()
    if created:
        Notification.objects.create(buyer=instance.order.user,seller=admin,delivery=instance,message=str(instance.order.user.username)+", Delivery for your order has been Created! ")
    else:
        state_change = True if 'state' in update_fields else False
        if state_change:
            Notification.objects.create(buyer=instance.order.user, seller=admin, delivery=instance,
                                        message=str(instance.order.user.username) + ",Delivery status has been Changed for " + str(instance.order.orderid))


@receiver(post_save,sender=Notification)
def notification_handler(sender,instance,created,**kwargs):
    #call group_send function directly to send notifications or you can create a dynamic task in celery beat
    print(">>>>>>>>>Notification Created\n\n\n",instance.created_at)
    if created:
        schedule, created = CrontabSchedule.objects.get_or_create(hour = instance.created_at.hour, minute = int(instance.created_at.minute+1 % 60), day_of_month = instance.created_at.day, month_of_year = instance.created_at.month,timezone='UTC')
        task = PeriodicTask.objects.create(crontab=schedule, name="broadcast-notification-"+str(instance.id), task="notifications_app.tasks.broadcast_notification", args=json.dumps((instance.id,)))
        