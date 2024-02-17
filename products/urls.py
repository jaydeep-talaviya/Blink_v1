from django.urls import path
from .views import (productlist,productdetail, return_policy,
                    submit_rates_and_comments,
                    productcart,productcartupdateremove,
                    checkout_details,userorders,
                    orderviews,html_to_pdf_view,
                    productlist_sortby,search,
                    cancle_order,
                    return_policy,terms_and_conditions,about,contact,create_order,
                    order_re_payment,
                    send_otp,match_otp,otp_order_failed,verified_created_order,get_discounted_price,
                    get_total_vouchers,callback)

urlpatterns = [
    path('search',search,name='search'),
    
    path('products/sorted_by',productlist_sortby,name='productlist_sortby'),
    path('products/<int:p_id>',productdetail,name='productdetail'),

    path('products/voucher-applied',get_discounted_price,name='applied_voucher'),
    path('products/product/cart',productcart,name='productcart'),
    path('cart/update',productcartupdateremove,name='productcartupdateremove'),
    path('checkout',checkout_details,name='checkout'),
    path('orders',userorders,name='userorders'),
    path('orders/<str:order_by>',userorders,name='userorders'),
    path('order/<str:orderid>',orderviews,name='orderviews'),
    path('receipt/<str:orderid>',html_to_pdf_view,name='receipt'),

    path('products',productlist,name='productlist'),
    path('products/<str:subcategory>',productlist,name='productlist'),

    path('rate_and_comment_submit',submit_rates_and_comments,name='submit_rates_and_comments'),

    path('cancle_order/<str:orderid>',cancle_order,name='cancle_order'),
    
    path('send_otp',send_otp,name='send_otp'),
    path('match_otp',match_otp,name='match_otp'),
    path('order-failed',otp_order_failed,name='otp_order_failed'),
    path('order-created',verified_created_order,name='verified_created_order'),
    
    path('return_policy',return_policy,name="return_policy"),
    path('terms_and_conditions',terms_and_conditions,name="terms_and_conditions"),
    path('about',about,name="about"),
    path('contact',contact,name="contact"),

    path('create_order',create_order,name="create_order"),
    path("razorpay/callback/", callback, name="callback"),

    path('order/repayment/<str:orderid>',order_re_payment,name="order_re_payment"),

    path("get/vouchers", get_total_vouchers, name="get_total_vouchers"),

]