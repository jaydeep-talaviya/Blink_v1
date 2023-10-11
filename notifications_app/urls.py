
from django.urls import path,include
from .views import test, single_delivery, delivery_list, change_notifications_status

urlpatterns = [
    path('testing', test,name='testing'),
    path('delivery/lists',delivery_list,name='delivery_list'),
    path('delivery/lists/<str:status>',delivery_list,name='delivery_list_with_status'),
    path('delivery/<str:delivery_id>',single_delivery,name='single_delivery'),
    path("notification/change/<int:notification_id>", change_notifications_status, name="change_notifications_status"),

]