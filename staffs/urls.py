from django.urls import path
from .views import (home,product_list,product_update,product_delete,
                    product_add,create_product_attribute,product_update_attribute,
                    create_attribute,update_attribute,remove_attribute,
                    create_attribute_name,product_attribute_list,
                    stock_list,stock_update,stock_create,
                    deals_of_day_list,create_deals_of_the_day,update_deals_of_the_day,
                    orderlists,single_order,paymentlists,
                    create_attribute_names,update_attribute_names,remove_attribute_names,list_attribute_name,
                    get_attribute_values,
                    create_category,update_category,list_category,remove_category,
                    create_sub_category,update_sub_category,list_sub_category,remove_sub_category,
create_voucher,list_vouchers
                    )

urlpatterns = [
    path('',home,name='staff_homepage'),
    path('product/',product_list,name='product_list'),
    path('product/add/',product_add,name='product_add'),
    path('product/update/<int:id>/',product_update,name='product_update'),
    path('product/delete/<int:id>/', product_delete, name='product_delete'),
    path('product/update/<int:pid>/attribute/create/',create_product_attribute,name='create_product_attribute'),
    path('product/update/<int:pid>/attribute/update/<int:id>/',product_update_attribute,name='product_update_attribute'),

    path('product/attribute/attribute/name/create/',create_attribute_names,name='create_attribute_names'),

    path('product/attribute/attribute/',product_attribute_list,name='product_attribute_list'),
    path('product/attribute/attribute/create/',create_attribute,name='create_attribute'),
    path('product/attribute/attribute/update/<int:id>/',update_attribute,name='update_attribute'),
    path('product/attribute/attribute/delete/<int:id>/',remove_attribute,name='remove_attribute'),

    path('product/attribute/name/', list_attribute_name, name='list_attribute_name'),
    path('product/attribute/name/create/',create_attribute_name,name='create_attribute_name'),
    path('product/attribute/name/update/<int:id>',update_attribute_names,name='update_attribute_names'),
    path('product/attribute/name/remove/<int:id>',remove_attribute_names,name='remove_attribute_names'),

    path('product/category/', list_category, name='list_category'),
    path('product/category/create/', create_category, name='create_category'),
    path('product/category/update/<int:id>', update_category, name='update_category'),
    path('product/category/remove/<int:id>', remove_category, name='remove_category'),

    path('product/subcategory/', list_sub_category, name='list_sub_category'),
    path('product/subcategory/create/', create_sub_category, name='create_sub_category'),
    path('product/subcategory/update/<int:id>', update_sub_category, name='update_sub_category'),
    path('product/subcategory/remove/<int:id>', remove_sub_category, name='remove_sub_category'),

    # ajax
    path('get_attribute_values/',get_attribute_values,name='get_attribute_values'),

    path('product/voucher/', list_vouchers, name='list_vouchers'),
    path('product/voucher/create/', create_voucher, name='create_voucher'),



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