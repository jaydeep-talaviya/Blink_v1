from django import template
import hashlib
from django.urls import reverse
from django.conf import settings

register = template.Library()

list_urls = ['', 'registration', 'login/', 'logout', 'profile/update', 'profileshow', 'profile/delete/<int:id>',
             'password-reset/', 'password-reset/done/', 'password-reset-confirm/<uidb64>/<token>/',
             'password-reset-complete/', 'password-change', 'accounts/signup/', 'accounts/login/',
             'accounts/logout/', 'accounts/password/change/', 'accounts/password/set/', 'accounts/inactive/',
             'accounts/email/', 'accounts/confirm-email/', 'accounts/^confirm-email/(?P<key>[-:\\w]+)/$',
             'accounts/password/reset/', 'accounts/password/reset/done/',
             'accounts/^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$',
             'accounts/password/reset/key/done/', 'accounts/social/login/cancelled/',
             'accounts/social/login/error/', 'accounts/social/signup/',
             'accounts/social/connections/', 'accounts/google/login/',
             'accounts/google/login/callback/', 'accounts/facebook/login/',
             'accounts/facebook/login/callback/', 'accounts/facebook/login/token/',
             'search', 'products/sorted_by', 'products/<int:p_id>',
             'products/voucher-applied', 'products/product/cart', 'cart/update',
             'checkout', 'orders', 'orders/<str:order_by>', 'order/<str:orderid>',
             'receipt/<str:orderid>', 'products', 'products/<str:subcategory>', 'rate_and_comment_submit',
             'cancle_order/<str:orderid>', 'send_otp', 'match_otp', 'order-failed', 'order-created', 'return_policy',
             'terms_and_conditions', 'about', 'contact', 'create_order', 'razorpay/callback/',
             'order/repayment/<str:orderid>', 'get/vouchers', 'admin/', 'admin/user/admin/logs/',
             'admin/user/employee_report/', 'admin/product/', 'admin/product/<str:type>', 'admin/product/add/',
             'admin/product/create/', 'admin/product/edit/<int:id>/', 'admin/product/update/<int:id>/',
             'admin/product/delete/<int:id>/', 'admin/product/verify/<int:id>/<str:type>',
             'admin/attribute/attribute/name/create/', 'admin/attribute/attribute/',
             'admin/attribute/attribute/create/', 'admin/attribute/attribute/update/<int:id>/',
             'admin/attribute/attribute/delete/<int:id>/', 'admin/attribute/name/', 'admin/attribute/name/create/',
             'admin/attribute/name/update/<int:id>', 'admin/attribute/name/remove/<int:id>', 'admin/category/',
             'admin/category/create/', 'admin/category/update/<int:id>', 'admin/category/remove/<int:id>',
             'admin/subcategory/', 'admin/subcategory/create/', 'admin/subcategory/update/<int:id>',
             'admin/subcategory/remove/<int:id>', 'admin/get_attribute_values/', 'admin/voucher/',
             'admin/voucher/create/', 'admin/voucher/update/<int:id>',
             'admin/voucher/update/status/<int:id>/<int:type>', 'admin/voucher/delete/<int:id>', 'admin/stocks/',
             'admin/stock/warehouse/select/', 'admin/stock/warehouse/product/select/', 'admin/stock/info/managers/',
             'admin/stocks/create/', 'admin/stocks/update/<int:id>', 'admin/stocks/finish/<int:id>',
             'admin/orders/single/<str:order_id>', 'admin/orders/', 'admin/orders/<str:status>', 'admin/payments/',
             'admin/payments/<str:status>', 'admin/employee/', 'admin/employee/create/', 'admin/employee/update/<int:id>',
             'admin/employee/remove/<int:id>', 'admin/employee/salary/create/<int:id>',
             'admin/employee/salary/update/<int:id>', 'admin/employee/salary/delete/<int:id>',
             'admin/employee/salary/<int:id>', 'admin/warehouse/', 'admin/warehouse/create/',
             'admin/warehouse/update/<int:id>', 'admin/warehouse/remove/<int:id>', 'admin/warehouse/deleted/',
             'admin/warehouse/approval/', 'admin/warehouse/approvel/<int:id>/<str:type>', 'admin/prepare_order/',
             'admin/prepare_products/select/', 'admin/prepare_order/create/<str:order_id>',
             'admin/prepare_order/update/<str:orderid>', 'admin/prepare_order/delivery/create/<str:orderid>',
             'admin/order/delivery/', 'admin/order/delivery/verify/<str:delivery_id>', 'admin/order/delivery/cancel/<str:orderid>',
             'admin/ledger/list/', 'admin/ledger/list/<str:type>', 'admin/ledger/create/', 'admin/ledger/update/<int:id>',
             'admin/delivery/lists', 'admin/delivery/lists/<str:status>',
             'admin/delivery/<str:delivery_id>', 'admin/notification/change/<int:notification_id>',
             '^static/(?P<path>.*)$', '^media/(?P<path>.*)$']


@register.filter(name='check_url_exists')
def check_url_exists(url):
    print(">>>>>url....",url)
    try:
        # reverse(url)
        # print(reverse(url))
        if url[1:] in list_urls or url[1:]+'/' in list_urls:
            print("The endpoint exists.",url)
            return True
        else:
            print("The endpoint does not exist.",url)
            return False
    except Exception as e:
        print(">>>>>>error",e)
        return False
