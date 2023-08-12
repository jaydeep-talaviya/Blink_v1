from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
import json
from celery import Celery, states
from celery.exceptions import Ignore
import asyncio
 
print("....aaaaaabbbbcc111111111............\n\n\n\n\n")

@shared_task(bind = True)
def broadcast_notification(self, data):
    try:
        notification = Notification.objects.filter(id = int(data))
        if len(notification)>0:
            notification = notification.first()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notification_"+notification.seller.username,
                {
                    'type': 'send_notification',
                    'message': json.dumps(
                        {'message':notification.message,
                        'delivery_id':notification.delivery.delivery_id
                        }
                        ),
                }
            )
            notification.sent = True
            notification.save()
            return 'Done'

        else:
            self.update_state(
                state = 'FAILURE',
                meta = {'exe': "Not Found"}
            )

            raise Ignore()

    except:
        self.update_state(
                state = 'FAILURE',
                meta = {
                        'exe': "Failed"
                        # 'exc_type': type(ex).__name__,
                        # 'exc_message': traceback.format_exc().split('\n')
                        # 'custom': '...'
                    }
            )

        raise Ignore()
