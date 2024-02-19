from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from utils.helper_functions import encrypt_value
from .models import Notification
import json
from celery import Celery, states
from celery.exceptions import Ignore
import asyncio
 
print("....aaaaaabbbbcc111111111............\n\n\n\n\n")

@shared_task(bind = True)
def broadcast_notification(self, data):
    print(">>>>>>>>>step 11111111111111",data)
    try:
        notification = Notification.objects.filter(id = int(data))
        print(">>>>>>>>>step 2222222222",notification)

        if notification.exists()>0:
            print(">>>>>>>>>step 333333333333", notification)

            notification = notification.first()
            channel_layer = get_channel_layer()
            print(">>>>>>>>>step channel_layer", channel_layer,channel_layer.group_send)
            # condition to check send notification to user or admin
            username = encrypt_value(str(notification.receiver.username)+"_"+str(notification.receiver.id))
            print(">>>>username",username)
            async_to_sync(channel_layer.group_send)(
                "notification_"+username,
                {
                    'type': 'send_notification',
                    'message': json.dumps(
                        {'message':notification.message,
                         "related_url":notification.related_url
                        }
                        ),
                }
            )
            # notification.sent = True
            notification.save()
            return 'Done'

        else:
            self.update_state(
                state = 'FAILURE',
                meta = {'exe': "Not Found"}
            )

            raise Ignore()

    except Exception as e:
        print(e,">>>>>>>error\n\n\n")
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
