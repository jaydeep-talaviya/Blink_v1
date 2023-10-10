from .models import Notification
from users.models import User
from datetime import datetime

def notifications(request):
    if request.user.is_authenticated:
        admin = User.objects.filter(is_superuser=True).first()
        admin_notifications = Notification.objects.filter(seller=admin)
        end_user_notifications = Notification.objects.filter(buyer=request.user)

        return {'admin_notifications': admin_notifications,'end_user_notifications':end_user_notifications}
    else:
        return {'notifications':[]}