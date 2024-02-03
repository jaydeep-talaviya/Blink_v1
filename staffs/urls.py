from django.urls import path
from .views import (product_list, product_update, product_delete,
                    product_create, create_product_attribute, product_update_attribute,
                    create_attribute, update_attribute, remove_attribute,
                    create_attr_name, product_attribute_list,
                    stock_list, stock_update, stock_create, stock_finish, inform_other_managers,
                    orderlists, single_order, paymentlists,
                    create_attribute_names, update_attribute_names, remove_attribute_names, list_attribute_name,
                    get_attribute_values,
                    create_category, update_category, list_category, remove_category,
                    create_sub_category, update_sub_category, list_sub_category, remove_sub_category,
                    create_voucher, list_vouchers, update_voucher, delete_voucher, update_status_voucher,
                    create_employee, list_employees, update_employee, delete_employee,
                    create_employee_salary, employee_salary_list, update_employee_salary, delete_employee_salary,
                    create_warehouse, list_warehouses, update_warehouse, delete_warehouse, list_deleted_warehouses,
                    approve_or_cancel_warehouse, list_approval_need_warehouses,
                    prepare_order, prepare_order_dynamic_content,
                    get_product_by_warehouse, get_product_attrs_by_product_warehouse,
                    list_prepare_orders, create_delivery, update_prepare_order,
                    list_of_ledgers, create_other_ledgers, update_other_ledgers,
                    custom_log_view, dashboard, get_employees_download
                    )

urlpatterns = [

    path('', dashboard, name='dashboard'),
    path('user/admin/logs/', custom_log_view, name='custom_log_view'),
    path('user/employee_report/', get_employees_download, name='get_employees_download'),

    path('product/',product_list,name='product_list'),
    path('product/add/',product_create,name='product_create'),
    path('product/update/<int:id>/',product_update,name='product_update'),
    path('product/delete/<int:id>/', product_delete, name='product_delete'),
    path('product/update/<int:pid>/attribute/create/',create_product_attribute,name='create_product_attribute'),
    path('product/update/<int:pid>/attribute/update/<int:id>/',product_update_attribute,name='product_update_attribute'),

    path('attribute/attribute/name/create/',create_attribute_names,name='create_attribute_names'),

    path('attribute/attribute/',product_attribute_list,name='product_attribute_list'),
    path('attribute/attribute/create/',create_attribute,name='create_attribute'),
    path('attribute/attribute/update/<int:id>/',update_attribute,name='update_attribute'),
    path('attribute/attribute/delete/<int:id>/',remove_attribute,name='remove_attribute'),

    path('attribute/name/', list_attribute_name, name='list_attribute_name'),
    path('attribute/name/create/',create_attr_name,name='create_attr_name'),
    path('attribute/name/update/<int:id>',update_attribute_names,name='update_attribute_names'),
    path('attribute/name/remove/<int:id>',remove_attribute_names,name='remove_attribute_names'),

    path('category/', list_category, name='list_category'),
    path('category/create/', create_category, name='create_category'),
    path('category/update/<int:id>', update_category, name='update_category'),
    path('category/remove/<int:id>', remove_category, name='remove_category'),

    path('subcategory/', list_sub_category, name='list_sub_category'),
    path('subcategory/create/', create_sub_category, name='create_sub_category'),
    path('subcategory/update/<int:id>', update_sub_category, name='update_sub_category'),
    path('subcategory/remove/<int:id>', remove_sub_category, name='remove_sub_category'),

    # ajax
    path('get_attribute_values/',get_attribute_values,name='get_attribute_values'),

    path('voucher/', list_vouchers, name='list_vouchers'),
    path('voucher/create/', create_voucher, name='create_voucher'),
    path('voucher/update/<int:id>', update_voucher, name='update_voucher'),
    path('voucher/update/status/<int:id>/<int:type>', update_status_voucher, name='update_status_voucher'),
    path('voucher/delete/<int:id>', delete_voucher, name='delete_voucher'),



    path('stocks/',stock_list,name='stock_list'),
    path('stock/warehouse/select/', get_product_by_warehouse, name='get_product_by_warehouse'),
    path('stock/warehouse/product/select/', get_product_attrs_by_product_warehouse, name='get_product_attrs_by_product_warehouse'),
    path('stock/info/managers/',inform_other_managers,name='inform_other_managers'),
    path('stocks/create/',stock_create,name='stock_create'),
    path('stocks/update/<int:id>',stock_update,name='stock_update'),
    path('stocks/finish/<int:id>',stock_finish,name='stock_finish'),


    path('orders/single/<str:order_id>',single_order,name='single_order'),

    path('orders/',orderlists,name='orderlists'),
    path('orders/<str:status>',orderlists,name='orderlists_with_status'),


    path('payments/',paymentlists,name='paymentlists'),
    path('payments/<str:status>',paymentlists,name='paymentlists_with_status'),

    ##### employee #####
    path('employee/', list_employees, name='list_employees'),
    path('employee/create/', create_employee, name='create_employee'),
    path('employee/update/<int:id>', update_employee, name='update_employee'),
    path('employee/remove/<int:id>', delete_employee, name='delete_employee'),

    path('employee/salary/create/<int:id>', create_employee_salary, name='create_employee_salary'),
    path('employee/salary/update/<int:id>', update_employee_salary, name='update_employee_salary'),
    path('employee/salary/delete/<int:id>', delete_employee_salary, name='delete_employee_salary'),
    path('employee/salary/<int:id>', employee_salary_list, name='employee_salary_list'),

    ##### warehouse #####
    path('warehouse/', list_warehouses, name='list_warehouses'),
    path('warehouse/create/', create_warehouse, name='create_warehouse'),
    path('warehouse/update/<int:id>', update_warehouse, name='update_warehouse'),
    path('warehouse/remove/<int:id>', delete_warehouse, name='delete_warehouse'),
    path('warehouse/deleted/', list_deleted_warehouses, name='list_deleted_warehouses'),
    path('warehouse/approval/', list_approval_need_warehouses, name='list_approval_need_warehouses'),
    path('warehouse/approvel/<int:id>/<str:type>', approve_or_cancel_warehouse, name='approve_or_cancel_warehouse'),

    #### prepare orders
    path('prepare_order/', list_prepare_orders, name='list_prepare_orders'),
    path('prepare_products/select/',prepare_order_dynamic_content,name='prepare_order_dynamic_content'),
    path('prepare_order/create/<str:order_id>',prepare_order,name='prepare_order'),
    path('prepare_order/update/<str:orderid>',update_prepare_order,name='update_prepare_order'),

    path('prepare_order/delivery/create/<str:orderid>', create_delivery, name='create_delivery'),

    # get Product from Product maker and add to warehouse
    path('ledger/list/', list_of_ledgers, name='list_of_ledgers'),
    path('ledger/list/<str:type>',list_of_ledgers,name='list_of_ledgers'),
    path('ledger/create/', create_other_ledgers, name='create_other_ledgers'),
    path('ledger/update/<int:id>', update_other_ledgers, name='update_other_ledgers'),



]