from .models import Notification
from users.models import User
from datetime import datetime

def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(receiver=request.user).order_by('-created_at')
        read_notifications_count = notifications.filter(is_read=False).count()

        return {'notifications': notifications,'read_notifications_count':read_notifications_count}
    else:
        return {'notifications':[]}