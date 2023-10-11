from .models import Notification
from users.models import User
from datetime import datetime

def notifications(request):
    if request.user.is_authenticated:
        admin = User.objects.filter(is_superuser=True).first()
        admin_notifications = Notification.objects.filter(seller=admin)
        read_admin_notifications_count = Notification.objects.filter(seller=admin,is_checked=False).count()
        end_user_notifications = Notification.objects.filter(buyer=request.user)
        read_end_user_notifications_count = Notification.objects.filter(buyer=request.user,is_checked=False).count()
        return {'admin_notifications': admin_notifications,'read_admin_notifications_count':read_admin_notifications_count,
                'end_user_notifications':end_user_notifications,'read_end_user_notifications_count':read_end_user_notifications_count}
    else:
        return {'notifications':[]}