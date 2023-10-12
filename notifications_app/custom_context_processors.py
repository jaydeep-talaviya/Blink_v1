from .models import Notification
from users.models import User
from datetime import datetime

def notifications(request):
    if request.user.is_authenticated:
        admin = User.objects.filter(is_superuser=True).first()
        admin_notifications = Notification.objects.filter(seller=admin,for_admin = True)
        read_admin_notifications_count = admin_notifications.filter(is_checked=False).count()
        end_user_notifications = Notification.objects.filter(buyer=request.user,for_customer=True)
        read_end_user_notifications_count = end_user_notifications.filter(is_checked=False).count()
        return {'admin_notifications': admin_notifications,'read_admin_notifications_count':read_admin_notifications_count,
                'end_user_notifications':end_user_notifications,'read_end_user_notifications_count':read_end_user_notifications_count}
    else:
        return {'notifications':[]}