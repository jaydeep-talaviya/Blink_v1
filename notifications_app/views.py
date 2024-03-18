import datetime
import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from channels.layers import get_channel_layer
import json

from notifications_app.models import Notification
from products.models import Delivery
from django.contrib import messages

# Create your views here.

from asgiref.sync import async_to_sync

from utils.helper_functions import get_pagination_records, send_email_to_notify_customer, get_related_url


# def test(request):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         "notification_jay",
#         {
#             'type': 'send_notification',
#             'message': json.dumps(
#                         {'message':'asdfasdfasd',
#                         'delivery_id':'asdfas2121'
#                         }
#                         ),
#         }
#     )
#     return HttpResponse("Done")


@login_required
def change_notifications_status(request,notification_id):
    notification = Notification.objects.get(id = notification_id)
    notification.is_read = True
    notification.save()
    return redirect(notification.related_url)


def single_delivery(request,delivery_id):

    delivery=Delivery.objects.get(delivery_id=delivery_id)
    customer = delivery.order.user
    order = delivery.order

    if request.method == 'POST':
        delivery_status=request.POST.get('delivery_status')
        if delivery_status == 'Confirm' and delivery.state not in ['Confirm','Started','Delivering','Shipped']:
            delivery.state=delivery_status
            delivery.updated_at = datetime.datetime.now()
            delivery.otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            delivery.save()
        if delivery_status == 'Started' and delivery.state not in ['Started','Delivering','Shipped']:
            delivery.state=delivery_status
            delivery.updated_at = datetime.datetime.now()
            delivery.save()
        elif delivery_status == 'Delivering' and delivery.state not in ['Delivering','Shipped']:
            delivery.state = delivery_status
            delivery.updated_at = datetime.datetime.now()
            delivery.save()
            send_email_to_notify_customer(customer,order,delivery.otp_code)
        elif delivery_status == 'Shipped' and delivery.state not in ['Shipped'] and delivery.state == 'Delivering':
            delivery.state = delivery_status
            delivery.delivered_at = datetime.datetime.now()
            delivery.save()
            related_url = get_related_url(request, 'delivery',id=delivery_id)
            Notification.objects.create(sender=request.user, receiver=customer,
                                        message='Please Check Yout Items,Your Order has been Shipped!',
                                        related_url=related_url
                                        )
            if (request.user.is_authenticated and (hasattr(request.user, 'employee') and request.user.employee.type == 'delivery_person')):
                return redirect('delivery_orders')
        else:
            messages.warning(request,('You must select Delivery status based on previous delivery'))
    return render(request,'notifications_app/single_delivery.html',{'delivery':delivery})

def delivery_list(request,status=None):
    print(">>>\n\n\n",request.user.id)
    deliveries = Delivery.objects.filter(delivery_person=request.user)
    if request.user.is_superuser or (hasattr(request.user, 'employee') and request.user.employee.type == 'manager'):
        deliveries = Delivery.objects.all()
    if status:
        deliveries = deliveries.filter(state=status)

    deliveries = get_pagination_records(request,deliveries)

    return render(request,'notifications_app/delivery_lists.html',{'deliveries':deliveries,'Status':status})
