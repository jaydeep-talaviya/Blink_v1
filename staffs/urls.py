from django.urls import path
from .views import (home,product_list,product_update,
                    product_add,create_product_attribute,product_update_attribute,
                    create_attribute,update_attribute,create_attribute_name,product_attribute_list,
                    stock_list,stock_update,stock_create,
                    deals_of_day_list,create_deals_of_the_day,update_deals_of_the_day,
                    orderlists,single_order,paymentlists
                    )

urlpatterns = [
    path('',home,name='staff_homepage'),
    path('product/',product_list,name='product_list'),
    path('product/add/',product_add,name='product_add'),
    path('product/update/<int:id>/',product_update,name='product_update'),
    path('product/update/<int:pid>/attribute/create/',create_product_attribute,name='create_product_attribute'),
    path('product/update/<int:pid>/attribute/update/<int:id>/',product_update_attribute,name='product_update_attribute'),

    path('product/attribute/attribute/',product_attribute_list,name='product_attribute_list'),
    path('product/attribute/attribute/create/',create_attribute,name='create_attribute'),
    path('product/attribute/attribute/update/<int:id>/',update_attribute,name='update_attribute'),

    path('product/attribute/name/create/',create_attribute_name,name='create_attribute_name'),

    path('product/stocks/',stock_list,name='stock_list'),
    path('product/stocks/create/',stock_create,name='stock_create'),

    path('product/stocks/update/<int:id>',stock_update,name='stock_update'),

    path('product/today_deals/',deals_of_day_list,name='deals_of_day_list'),
    path('product/today_deals/create',create_deals_of_the_day,name='create_deals_of_the_day'),
    path('product/today_deals/update/<int:id>',update_deals_of_the_day,name='update_deals_of_the_day'),

    path('product/orders/single/<str:order_id>',single_order,name='single_order'),

    path('product/orders/',orderlists,name='orderlists'),
    path('product/orders/<str:status>',orderlists,name='orderlists_with_status'),


    path('product/payments/',paymentlists,name='paymentlists'),
    path('product/payments/<str:status>',paymentlists,name='paymentlists_with_status'),


]