from django.urls import path
from .views import (productlist,productdetail, return_policy,
                    submit_rates_and_comments,
                    productcart,productcartupdateremove,
                    checkout_details,userorders,
                    orderviews,html_to_pdf_view,
                    productlist_sortby,search,
                    cancelorder,
                    return_policy,terms_and_conditions,about,contact,createorder,
                    handlerequest,update_order,
                    send_otp,match_otp,order_failed,order_created,get_discounted_price)

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

    path('cancelorder/<str:orderid>',cancelorder,name='cancelorder'),
    
    path('send_otp',send_otp,name='send_otp'),
    path('match_otp',match_otp,name='match_otp'),
    path('order-failed',order_failed,name='order_failed'),
    path('order-created',order_created,name='order_created'),
    
    path('return_policy',return_policy,name="return_policy"),
    path('terms_and_conditions',terms_and_conditions,name="terms_and_conditions"),
    path('about',about,name="about"),
    path('contact',contact,name="contact"),

    path('createorder',createorder,name="createorder"),
    path("handlerequest", handlerequest, name="HandleRequest"),
    path('update_order/<str:orderid>',update_order,name="update_order")
]