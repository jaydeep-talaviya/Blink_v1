from .models import Notification
from users.models import User
from datetime import datetime

def notifications(request):
    if request.user.is_authenticated:
        allnotifications = Notification.objects.filter(seller=request.user,created_at__date=datetime.now().today())
        # hour = instance.created_at.hour, minute = int(instance.created_at.minute+2 % 60), day_of_month = instance.created_at.day, month_of_year = instance.created_at.month
        return {'notifications': allnotifications}
    else:
        return {'notifications':[]}