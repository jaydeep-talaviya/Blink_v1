from django.urls import path
from .views import (home, product_list, product_update, product_delete,
                    product_add, create_product_attribute, product_update_attribute,
                    create_attribute, update_attribute, remove_attribute,
                    create_attribute_name, product_attribute_list,
                    stock_list, stock_update, stock_create,stock_finish,
                    deals_of_day_list, create_deals_of_the_day, update_deals_of_the_day,
                    orderlists, single_order, paymentlists,
                    create_attribute_names, update_attribute_names, remove_attribute_names, list_attribute_name,
                    get_attribute_values,
                    create_category, update_category, list_category, remove_category,
                    create_sub_category, update_sub_category, list_sub_category, remove_sub_category,
                    create_voucher, list_vouchers, update_voucher, delete_voucher, update_status_voucher,
                    create_employee,list_employees,update_employee,delete_employee,
                    create_warehouse,list_warehouses,update_warehouse,delete_warehouse,
                    prepare_order,prepare_order_dynamic_content,
                    get_product_by_warehouse,get_product_attrs_by_product_warehouse
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
    path('product/voucher/update/<int:id>', update_voucher, name='update_voucher'),
    path('product/voucher/update/status/<int:id>/<int:type>', update_status_voucher, name='update_status_voucher'),
    path('product/voucher/delete/<int:id>', delete_voucher, name='delete_voucher'),



    path('product/stocks/',stock_list,name='stock_list'),
    path('product/stock/warehouse/select/', get_product_by_warehouse, name='get_product_by_warehouse'),
    path('product/stock/warehouse/product/select/', get_product_attrs_by_product_warehouse, name='get_product_attrs_by_product_warehouse'),
    path('product/stocks/create/',stock_create,name='stock_create'),
    path('product/stocks/update/<int:id>',stock_update,name='stock_update'),
    path('product/stocks/finish/<int:id>',stock_finish,name='stock_finish'),



    path('product/today_deals/',deals_of_day_list,name='deals_of_day_list'),
    path('product/today_deals/create',create_deals_of_the_day,name='create_deals_of_the_day'),
    path('product/today_deals/update/<int:id>',update_deals_of_the_day,name='update_deals_of_the_day'),

    path('product/orders/single/<str:order_id>',single_order,name='single_order'),

    path('product/orders/',orderlists,name='orderlists'),
    path('product/orders/<str:status>',orderlists,name='orderlists_with_status'),


    path('product/payments/',paymentlists,name='paymentlists'),
    path('product/payments/<str:status>',paymentlists,name='paymentlists_with_status'),

    ##### employee #####
    path('product/employee/', list_employees, name='list_employees'),
    path('product/employee/create/', create_employee, name='create_employee'),
    path('product/employee/update/<int:id>', update_employee, name='update_employee'),
    path('product/employee/remove/<int:id>', delete_employee, name='delete_employee'),

    ##### warehouse #####
    path('product/warehouse/', list_warehouses, name='list_warehouses'),
    path('product/warehouse/create/', create_warehouse, name='create_warehouse'),
    path('product/warehouse/update/<int:id>', update_warehouse, name='update_warehouse'),
    path('product/warehouse/remove/<int:id>', delete_warehouse, name='delete_warehouse'),

    path('product/prepare/products/select/',prepare_order_dynamic_content,name='prepare_order_dynamic_content'),
    path('product/prepare/order/create/',prepare_order,name='prepare_order'),

]