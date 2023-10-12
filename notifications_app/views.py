import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from channels.layers import get_channel_layer
import json

from notifications_app.models import Notification
from products.models import Delivery
from django.contrib import messages

# Create your views here.

from asgiref.sync import async_to_sync

from utils.helper_functions import get_pagination_records


def test(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_jay",
        {
            'type': 'send_notification',
            'message': json.dumps(
                        {'message':'asdfasdfasd',
                        'delivery_id':'asdfas2121'
                        }
                        ),
        }
    )
    return HttpResponse("Done")


@login_required
def change_notifications_status(request,notification_id):
    notification = Notification.objects.get(id = notification_id)
    notification.is_checked = True
    notification.save()
    if notification.for_customer:
        orderid = notification.delivery.order.orderid
        return redirect('orderviews',orderid=orderid)
    else:
        return redirect('prepare_order')


def single_delivery(request,delivery_id):

    delivery=Delivery.objects.get(delivery_id=delivery_id)
    if request.method == 'POST':
        delivery_status=request.POST.get('delivery_status')
        if delivery_status == 'Confirm' and delivery.state not in ['Confirm','Delivering','Shipped']:
            delivery.state=delivery_status
            delivery.updated_at = datetime.datetime.now()
            delivery.save()
        elif delivery_status == 'Delivering' and delivery.state not in ['Delivering','Shipped']:
            delivery.state = delivery_status
            delivery.updated_at = datetime.datetime.now()
            delivery.save()
        elif delivery_status == 'Shipped' and delivery.state not in ['Shipped'] and delivery.state == 'Delivering':
            delivery.state = delivery_status
            delivery.delivered_at = datetime.datetime.now()
            delivery.save()
        else:
            messages.warning(request,('You must select Delivery status based on previous delivery'))
    return render(request,'notifications_app/single_delivery.html',{'delivery':delivery})

def delivery_list(request,status='Confirm'):
    deliveries=Delivery.objects.filter(state=status)
    deliveries = get_pagination_records(request,deliveries)

    return render(request,'notifications_app/delivery_lists.html',{'deliveries':deliveries,'Status':status})
