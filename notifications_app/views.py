from django.shortcuts import render, HttpResponse
from channels.layers import get_channel_layer
import json
from products.models import Delivery
from datetime import datetime

# Create your views here.

from asgiref.sync import async_to_sync
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

def single_delivery(request,delivery_id):
    delivery=Delivery.objects.get(delivery_id=delivery_id)
    if request.method == 'POST':
        delivery_status=request.POST.get('delivery_status')
        delivery.state=delivery_status
        delivery.save()
    return render(request,'notifications_app/single_delivery.html',{'delivery':delivery})

def delivery_list(request,status='Confirm'):
    deliveries=Delivery.objects.filter(order__created_seller=request.user,created_at__date=datetime.now().today(),state=status)
    return render(request,'notifications_app/delivery_lists.html',{'deliveries':deliveries,'Status':status})
