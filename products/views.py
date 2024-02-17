import json
from datetime import datetime

import razorpay
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from ecommerce_blink.settings import MERCHANT_KEY, RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
from notifications_app.models import Notification
from utils.helper_functions import get_voucher_discount, get_paginator, get_related_url
from .models import Payment, Stocks, Checkout, OrderLines, Orders, Products, Rates, AttributeName, Cart, OtpModel, \
    Vouchers, Transaction
from django.db.models import Avg,Count,Max,Min
from users.models import User, Employee
from django.urls import reverse
from .forms import CheckoutForm
from django.http import JsonResponse
from django.db.models import Q,Min
from django.contrib.auth.decorators import login_required

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string

from datetime import timedelta

import smtplib
import random

from weasyprint import HTML
from . import Checksum
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from datetime import date
from django.templatetags.static import static

today = date.today()


def search(request):        
    if request.method == 'GET': # this will be GET now      
        product_search =  request.GET.get('search') # do some research what it does    
    subcategory="All"

    all_products=Products.objects.filter(Q(p_subcategory__subcategory_name__icontains=product_search)|Q(p_category__category_name__icontains=product_search) | Q(p_name__icontains=product_search))
    all_products.filter(is_deleted = False)
    minvalue=all_products.aggregate(Min('price'))
    maxvalue=all_products.aggregate(Max('price'))
    page = request.GET.get('page',1)   
    paginator = Paginator(all_products, 10)
    all_products = get_paginator(paginator,page)

    messages.info(request, f"Your Search For: {product_search}")

    return render(request, 'products/productlist.html',{'products':all_products,'result_for':subcategory,'minvalue':minvalue,'maxvalue':maxvalue})


def productlist(request,subcategory=None):
    page = request.GET.get('page',1)
    if subcategory == None:
        all_products=Products.objects.filter(productchangepriceattributes__isnull=False,is_qa_verified=True,is_deleted=False).distinct().order_by('price')
        subcategory='All'
    else:
        all_products=Products.objects.filter(productchangepriceattributes__isnull=False,is_qa_verified=True,is_deleted=False).filter((Q(p_subcategory__subcategory_name=subcategory)|Q(p_category__category_name=subcategory)) & Q(productchangepriceattributes__isnull=False,is_qa_verified=True)).distinct().order_by('price')
    minvalue=all_products.aggregate(Min('price'))
    maxvalue=all_products.aggregate(Max('price'))

    paginator = Paginator(all_products, 10)
    all_products = get_paginator(paginator,page)
    return render(request, 'products/productlist.html',{'products':all_products,'result_for':subcategory,'minvalue':minvalue,'maxvalue':maxvalue})

def productlist_sortby(request):

    if request.method == "GET":
        page = request.GET.get('page',1)

        sort_by=request.GET.get('sort_by',False)
        subcategory=request.GET.get('subcategory',False)
        all_products=Products.objects.filter(productchangepriceattributes__isnull=False,is_qa_verified=True,is_deleted=False)

        if subcategory == 'All' or None:
            all_products=all_products.order_by('price')
            subcategory='All'
        else:
            all_products=all_products.filter(Q(p_subcategory__subcategory_name=subcategory)|Q(p_category__category_name=subcategory)).order_by('price')

        if sort_by != False:
            if sort_by == 'avg_rating':
                all_products=all_products.annotate(avg_rating=Avg('rates__rate')).order_by('-avg_rating')
            elif sort_by == 'popularity':
                all_products=all_products.annotate(rating_count=Count('rates__rate')).order_by('-rating_count')
            else:
                all_products=all_products.order_by(sort_by)
        else:
            minvalue=request.GET.get('minvalue',False)
            maxvalue=request.GET.get('maxvalue',False)
            all_products=all_products.filter(price__range=(minvalue, maxvalue))
        paginator = Paginator(all_products,10 )
        all_products = get_paginator(paginator, page)

    return render(request, 'products/productlist_temp.html',{'products':all_products})

def productdetail(request,p_id):
    products=Products.objects.get(id=p_id)
    product_attr_list=products.productchangepriceattributes_set.values('id','attribute_values__a_name__a_name','attribute_values__a_value','price')

    product_attr_dict={}
    prdct_varient={}
    for i in product_attr_list:
        if i['attribute_values__a_name__a_name'] not in prdct_varient:
            prdct_varient[i['attribute_values__a_name__a_name']] = [i['attribute_values__a_value']]
        else:
            if i['attribute_values__a_value'] not in prdct_varient[i['attribute_values__a_name__a_name']]:
                prdct_varient[i['attribute_values__a_name__a_name']]+=[i['attribute_values__a_value']]
        if i['attribute_values__a_name__a_name'] not in product_attr_dict:
            product_attr_dict[i['attribute_values__a_name__a_name']]=i['attribute_values__a_value']
        else:
            product_attr_dict[i['attribute_values__a_name__a_name']]+=','+i['attribute_values__a_value']
    #avg_rate
    product_avg_rate=products.rates_set.aggregate(Avg('rate'))['rate__avg'] if products.rates_set.values().count() != 0 else 0
    rate_list=['orange' for i in range(int(product_avg_rate))]+['black' for i in range(5-int(product_avg_rate))]

    # every rates and every comments
    product_comments_rate=list(products.rates_set.all().values()) if list(products.rates_set.all().values()) !=[] else []
    for i in product_comments_rate:
        get_user=User.objects.get(id=i['user_id'])
        i['user_id']=get_user
        i['rate']=['orange' for i in range(int(i['rate']))]+['black' for i in range(5-int(i['rate']))]

    on_above_purchase_vouchers = Vouchers.objects.filter(voucher_type='on_above_purchase',is_deleted=False)
    deals_of_day_voucher = Vouchers.objects.filter(voucher_type='deals_of_day',products__id=products.id,is_deleted=False)
    product_together_voucher = Vouchers.objects.filter(voucher_type='product_together',products__id=products.id,is_deleted=False)

    return render(request, 'products/productdetail.html',{'products':products,
                                                            'product_attr_list':product_attr_dict,
                                                            'prdct_varient':prdct_varient,'avg_rate':rate_list,
                                                            'product_comments_rate':product_comments_rate,
                                                            'deals':on_above_purchase_vouchers.union(product_together_voucher),
                                                            'deals_of_day_voucher':deals_of_day_voucher
                                                            })

@login_required
def submit_rates_and_comments(request):
    if request.method == "POST":
        products=Products.objects.get(id=request.POST.get('p_id',False))
        if len(Rates.objects.filter(Q(user=request.user) & Q(p_id=products))) == 0:
            rates_table=Rates.objects.create(comment=request.POST.get('comments',False),rate=request.POST.get('userRating',False),user=request.user,p_id=products)
            rates_table.save()
            product_comments_rate=list(products.rates_set.all().filter(id=rates_table.id).values()) if list(products.rates_set.all().filter(id=rates_table.id).values()) !=[] else []

        else:
            # message for error
            product_comments_rate=[]

        for i in product_comments_rate:
            get_user=User.objects.get(id=i['user_id'])
            i['user_id']=get_user
            i['rate']=['orange' for i in range(int(i['rate']))]+['black' for i in range(5-int(i['rate']))]

        return render(request, 'products/get_more_comments.html', {'product_comments_rate': product_comments_rate})
       
    else:
        return JsonResponse({"error": "please enter valid"}, status=400)



def get_discounted_price(request):
    user_cart_total_sum = sum([i['qty']*i['price'] for i in request.user.cart_set.values('qty','price')])
    voucher = Vouchers.objects.get(id=request.GET.get('id'))
    applied = False
    discount_amount =0
    try:
        discount_amount = get_voucher_discount(voucher,request.user,user_cart_total_sum)
    except Exception:
        print('>> something went wrong')
    if float(discount_amount) > 0:
        applied=True
        request.user.cart_set.update(vouchers= voucher)
    return JsonResponse({"discount_price": round(discount_amount,2),'applied':applied,"user_cart_total_sum":round(user_cart_total_sum,2)})

def get_total_vouchers(request):
    total_vouchers=Vouchers.objects.none()
    cart = Cart.objects.filter(user_id=request.user)
    if cart:
        products = list(cart.values_list('product_id', flat=True))
        user_cart_total_sum = sum([i['qty'] * i['price'] for i in request.user.cart_set.values('qty', 'price')])
        on_above_purchase_vouchers = Vouchers.objects.filter(voucher_type='on_above_purchase',on_above_purchase__lt=user_cart_total_sum,is_deleted=False)
        product_together_voucher = Vouchers.objects.filter(voucher_type='product_together', products__id__in=products,is_deleted=False)
        # promocode
        fixed_conditions = Q(voucher_type='promocode', users__id=request.user.id,
                             stop=False,is_deleted=False)  # Add your other fixed conditions here
        expirable_conditions = Q(expirable=True, expire_at__gt=datetime.now())
        user_used_conditions = ~Q(user_who_have_used=request.user.id)
        combined_conditions = fixed_conditions & expirable_conditions & user_used_conditions
        promocodes_vouchers = Vouchers.objects.filter(combined_conditions)
        total_vouchers = on_above_purchase_vouchers.union(product_together_voucher, promocodes_vouchers)
    return render(request, 'products/voucher_temp.html', {'vouchers': total_vouchers})


@login_required
def productcart(request):
    # promocode
    fixed_conditions = Q(voucher_type='promocode', users__id=request.user.id, stop=False,
                         is_deleted=False)  # Add your other fixed conditions here
    expirable_conditions = Q(expirable=True, expire_at__gt=datetime.now())
    user_used_conditions = ~Q(user_who_have_used=request.user.id)
    combined_conditions = fixed_conditions & expirable_conditions & user_used_conditions
    promocodes_vouchers = Vouchers.objects.filter(combined_conditions)
    if request.method=="POST":
        requestdata=dict(request.POST)
        product=Products.objects.get(id=int(requestdata.get('p_id')[0]))
        x=product.productchangepriceattributes_set

        selected_varient=''
        for i in requestdata.get('slct'):
            a_name=i.split('-')[0]
            a_value=i.split('-')[1]
            selected_varient=selected_varient+a_value+","
            x=x.filter(attribute_values__a_value=a_value,attribute_values__a_name__a_name=a_name)

        if len(x)!=0:
            price = x[0].price
            deals_of_day_voucher = Vouchers.objects.filter(voucher_type='deals_of_day', products__id=product.id,is_deleted=False)
            if deals_of_day_voucher:
                price = x[0].price - (price * deals_of_day_voucher.first().percent_off) / 100
            if len(Cart.objects.filter(Q(product_id=product) & Q(user_id=request.user) & Q(selected_product_varient=selected_varient)))==0:
                cart=Cart.objects.create(product_id=product,user_id=request.user,qty=1,selected_product_varient=selected_varient,price=price)
                messages.success(request, f"Your Cart is Ready")
            else:
                cart=Cart.objects.filter(Q(product_id=product) & Q(user_id=request.user) & Q(selected_product_varient=selected_varient))
                cart=cart.update(qty=cart[0].qty+1,price=price)
                messages.info(request, f"Your Cart is Updated")
        else:
            messages.error(request, f"product is unavailable with this varient")
            return redirect('productdetail',product.id)
        cart=Cart.objects.filter(user_id=request.user)

        on_above_purchase_vouchers = Vouchers.objects.filter(voucher_type='on_above_purchase',is_deleted=False)
        product_together_voucher = Vouchers.objects.filter(voucher_type='product_together', products__id__in=[product.id],is_deleted=False)
        total_vouchers = on_above_purchase_vouchers.union(product_together_voucher,promocodes_vouchers)

        return render(request,"products/cart.html",{'cart':cart,'vouchers':total_vouchers})

    else:
        cart=Cart.objects.filter(user_id=request.user)
        products = list(cart.values_list('product_id',flat=True))
        on_above_purchase_vouchers = Vouchers.objects.filter(voucher_type='on_above_purchase',is_deleted=False)
        product_together_voucher = Vouchers.objects.filter(voucher_type='product_together', products__id__in=products,is_deleted=False)
        total_vouchers = on_above_purchase_vouchers.union(product_together_voucher,promocodes_vouchers)
        return render(request,"products/cart.html",{'cart':cart,'vouchers':total_vouchers})

@login_required
def match_otp(request):
    otpmodel=OtpModel.objects.filter(user=request.user)

    if request.method == "POST":
        usr_otp=request.POST.get('otp_value')
        if usr_otp != False and usr_otp !='' and usr_otp==otpmodel.otp_number:
            otpmodel.update({'verified':True,'times':1})
            messages.success(request, f"Your Order is created! Please Check Your Orders")
            return redirect(verified_created_order)
        else:
            return JsonResponse({"warning":"Otp doesn't Matched,Please Try Again,"})
    else:
        return JsonResponse({"response":'okay'})
    # return render(request,"products/otp_validation.html")

@login_required
def otp_order_failed(request):
    otpmodel=OtpModel.objects.filter(user=request.user)
    otpmodel.update({'times':0})
    return render(request,'products/otp_order_failed.html')

@login_required
def verified_created_order(request):
    order=Orders.objects.filter(user=request.user).last()
    total_discount=[]
    orderlines=OrderLines.objects.filter(order_id__orderid=order.orderid)
    grand_total=order.amount
    order.save()
    return render(request,'products/new_order.html',{'order':order,'orderlines':orderlines,'total_discount':total_discount,"grand_total":grand_total})

@login_required
def send_otp(request):
    otp = random.randint(100000, 999999)
    otp = str(otp)
    otpmodel=OtpModel.objects.filter(user=request.user)
    if otpmodel.count() == 0:
        otpmodel=OtpModel.objects.create(user=request.user,otp_number=otp)
    else:
        otpmodel=otpmodel[0]
        otpmodel.otp_number=otp
        
    otpmodel.verified=False
    otpmodel.save()
    try:
        subject = f"Use OTP {otp} Dear {request.user.username}"
        message = f"""Use OTP {otp} to Confirm The Order. 
        Don't share it with someone else."""
        
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.user.email, ]
        send_mail( subject, message, email_from, recipient_list )

        otpmodel.times+=1
        otpmodel.save()
        messages.success(request, f"OTP sent succesfully On {request.user.email}")
    except:
        messages.error(request, f"Please enter the valid email address OR check an internet connection")
    return render(request,"products/otp_validation.html",{'times':otpmodel.times})

def return_policy(request):
    return render(request,"products/return_policy.html")
def terms_and_conditions(request):
    return render(request,"products/terms_and_conditions.html")

def about(request):
    return render(request,"products/about_us.html")

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        user_msg=request.POST.get('message')
        
        try:
            subject = f"User {name}'s Query"
            message = 'Subject: {}\n\n{}'.format(subject, user_msg)

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email,]
            send_mail(subject, message, email_from, recipient_list)
            admin = User.objects.filter(is_superuser=True).first()

            # Notification.objects.create(seller=admin,
            #                             message=' Please Check your mail, Someone with named ' + str(name) +' have reached out you',
            #                             for_admin=True)
            messages.success(request, "Message SuccessFully sent to admin,Thank You!")
        except:
            messages.error(request, "Something Went Wrong! Please Try again, Thank You")
        return render(request,"products/contact.html")

    if request.method=="GET":
        return render(request,"products/contact.html")


@login_required
def productcartupdateremove(request):
    if request.method == "GET":
        # get the nick name from the client side.
        cart_id = request.GET.get("cart_id", None)
        sign=request.GET.get("sign", None)
        cart=Cart.objects.get(id=cart_id)

        if sign == 'plus':
            cart.qty=cart.qty+1
        else:
            cart.qty=cart.qty-1
        cart.save()

        if cart.qty<=0:
            cart.delete()
        cart=Cart.objects.filter(user_id=request.user)
        return render(request, 'products/cart_temp.html', {'cart': cart})

@login_required
def create_order(request):
    cart=Cart.objects.filter(user_id=request.user)
    checkout=request.user.checkout_set.last()
    if len(cart)!=0 and checkout.payment_type == 'paytm':
        order = Orders.objects.create(checkout=checkout, order_status='order_confirm', user=request.user, amount=0,
                                       vouchers=cart.last().vouchers if cart.last().vouchers else None)
        amount=0
        for c in cart:
            OrderLines.objects.create(product_id=c.product_id, qty=c.qty, unit_price=c.price,
                                      sub_total_amount=c.qty * c.price, order_id=order,selected_product_varient=c.selected_product_varient)
            amount += c.qty * c.price

        voucher = cart.last().vouchers
        discount_amount = 0
        try:
            discount_amount = get_voucher_discount(voucher, request.user, amount)
        except Exception:
            print('>> something went wrong')
        amount=amount-discount_amount

        payment = Payment(user=order.user, order_id=order, payment_method='Online', status='Pending')
        payment.save()
        order.amount = amount
        order.total_discount = discount_amount
        order.payment_failed = False
        order.save()

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        print(">>>>>>>>>razorpay_order\n\n\n",razorpay_order)
        transaction = Transaction.objects.create(
            payment=payment, amount=amount, provider_order_id=razorpay_order.get('id')
        )
        transaction.save()
        param_dict={
                "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/",
                "razorpay_key": RAZORPAY_KEY_ID,
                "transaction": transaction,
                "order": order,
                'logo' : static('images/kimchi.png')
        }
        cart.delete()
        print(">>>>>>>>>>>\n\n\n",static('images/kimchi.png'))
        return render(request,"products/payment.html",param_dict)
    else:
        messages.error(request, "Something Went Wrong! Please Try again, Thank You")
    return redirect('checkout')


@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        result = client.utility.verify_payment_signature(response_data)
        print(">>>result",result)
        return result
    print(">>>>>>request",request.GET,request.POST)
    if "razorpay_signature" in request.POST:
        transaction_payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        transaction = Transaction.objects.get(provider_order_id=provider_order_id)
        transaction.transaction_payment_id = transaction_payment_id
        transaction.signature_id = signature_id
        transaction.save()
        print(">>>>>step 1....",request.POST)
        if verify_signature(request.POST):
            print(">>>>>step 2....")
            transaction.status = 'Success'
            transaction.save()
            payment=transaction.payment
            payment.status = "Success"
            payment.save()
            # send information to Manager that someone have created new Order
            if request.user.is_authenticated:
                managers = Employee.objects.filter(type='manager').values('user')
                related_url = get_related_url(request, 'product')

                # notify to each manager.
                for manager in managers:
                    Notification.objects.create(sender=request.user, receiver_id=manager.get('user'),
                                                message='New Order has been created! Please Prepare Order.',
                                                related_url=related_url
                                                )
            print(">>>>>>>>Notification Created On Order Payment success")
            return render(request, 'products/paymentstatus.html', {'response': transaction})

        else:
            print(">>>>>step 3....",request.POST)

            transaction.status = 'Failure'
            transaction.save()
            return render(request, 'products/paymentstatus.html', {'response': transaction})

    else:
        print(">>>>>step 4....",request.POST,type(request.POST))
        if dict(request.POST) == {}:
            messages.error(request,"Something Gets wrong!")
            return render(request, 'products/paymentstatus.html',{"response":None,"error":None})
        transaction_payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        transaction = Transaction.objects.get(provider_order_id=provider_order_id)
        transaction.transaction_payment_id = transaction_payment_id
        transaction.status = 'Failure'
        transaction.save()
        error = {
            "code":request.POST.get("error[code]"),
            "description":request.POST.get("error[description]"),
            "source":request.POST.get("error[source]"),
            "step":request.POST.get("error[step]"),
            "reason":request.POST.get("error[reason]"),

        }
        return render(request, 'products/paymentstatus.html', {'response': transaction,'error':error})

@login_required
def order_re_payment(request,orderid):
    order=Orders.objects.get(orderid=orderid)
    order.orderid=uuid.uuid4()
    order.save()
    payment = Payment(user=order.user, order_id=order, payment_method='Online', status='Pending')
    payment.save()

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order = client.order.create(
        {"amount": int(order.amount) * 100, "currency": "INR", "payment_capture": "1"}
    )
    transaction = Transaction(
        payment=payment, amount=order.amount, provider_order_id=razorpay_order.get('id')
    )
    transaction.save()
    param_dict = {
        "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/",
        "razorpay_key": RAZORPAY_KEY_ID,
        "transaction": transaction,
        "order": order,
        'logo': static('images/kimchi.png')
    }
    return render(request, 'products/payment.html',  param_dict)

@login_required
def checkout_details(request):
    checkout=Checkout.objects.filter(user=request.user)
    
    checkoutform=CheckoutForm()

    if request.method=='POST':
        if len(checkout)==0:
            form = CheckoutForm(request.POST or None, request.FILES or None)
            user=request.user
            
            if form.is_valid():
                if form.cleaned_data['payment_type']=='case_on_delivery':
                    form = form.save(commit=False) # Return an object without saving to the DB
                    form.user = request.user # Add an author field which will contain current user's id
                    form.save() # Save the final "real form" to the 
                    messages.success(request, "To Confirm Order ,Varify OTP")
                    return redirect('send_otp')
            # save the form data to model
                else:
                    return redirect("create_order")
                    # print("payment other types")
            else:
                messages.error(request, "Invalid Creadentials,Try Again")
                # print("invalid form")
            return render(request,'products/checkout.html',{'checkoutform':checkoutform})    

        else:
            checkout.update(first_name=request.POST.get('first_name'),
                            last_name=request.POST.get('last_name'),
                            address1=request.POST.get('address1'),
                            address2=request.POST.get('address2'),
                            state=request.POST.get('state'),
                            city=request.POST.get('city'),
                            zip=request.POST.get('zip'),
                            payment_type=request.POST.get('payment_type'))

            if request.POST.get('payment_type') == 'case_on_delivery':
                checkout[0].save()
                checkoutform=CheckoutForm(instance=checkout[0])
                messages.success(request, "To Confirm Order ,Varify OTP")
                return redirect('send_otp')    
            else:
                # messages.warning(request, "Please Try Again, Something Went Wrong!")
                messages.info(request, "Updated Form With Your New Changes")
                return redirect("create_order")
    else:
        try:
            checkoutform=CheckoutForm(instance=checkout[0])
        except Exception as e:
            checkoutform=CheckoutForm()
        messages.info(request, "Please Add Your Correct Shipping Address to Delivery Product")
        return render(request,'products/checkout.html',{'checkoutform':checkoutform})


@login_required
def userorders(request,order_by=None):
    page = request.GET.get('page',1)
    order_not_confirms=Orders.objects.filter(user=request.user,order_status='order_not_confirm').count()
    order_confirms=Orders.objects.filter(user=request.user,order_status='order_confirm').count()
    order_cancels=Orders.objects.filter(user=request.user,order_status='order_cancel').count()
    order_deliverings=Orders.objects.filter(user=request.user,order_status='order_delivering').count()
    order_shippeds=Orders.objects.filter(user=request.user,order_status='order_shipped').count()
    
    if order_by == None:
        allorders=Orders.objects.filter(user=request.user)
    else:
        allorders=Orders.objects.filter(user=request.user).filter(order_status=order_by)
    paginator = Paginator(allorders, 5)
    allorders = get_paginator(paginator, page)
    return render(request,'products/allorders.html',{'allorder':allorders,'order_not_confirms':order_not_confirms,'order_confirms':order_confirms,'order_cancels':order_cancels,'order_deliverings':order_deliverings,'order_shippeds':order_shippeds})

@login_required
def orderviews(request,orderid):
    order=Orders.objects.get(orderid=orderid)
    orderlines=OrderLines.objects.filter(order_id=order.id)
    today=datetime.now()
    return render(request,'products/order_views.html',{'today':today,'order':order,'orderlines':orderlines})

@login_required
def cancle_order(request,orderid):
    order=Orders.objects.get(orderid=orderid)
    order.order_status='order_cancel'
    order.save()
    managers = Employee.objects.filter(type='manager').values('user')
    related_url = get_related_url(request, 'order', id=orderid)

    # notify to each manager.
    for manager in managers:
        Notification.objects.create(sender=request.user, receiver_id=manager.get('user'),
                                    message='Order has been cancelled, Please check!',
                                    related_url=related_url
                                    )
    messages.error(request, "Your Order is Canceled Successfully!")
    return redirect('orderviews',orderid=order.orderid)

@login_required
def html_to_pdf_view(request,orderid):
    order=Orders.objects.get(orderid=orderid)
    orderlines=OrderLines.objects.filter(order_id=order.id)
    html_string = render_to_string('products/pdf_template.html', {'order':order,'orderlines':orderlines })

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/receipt.pdf')

    fs = FileSystemStorage('/tmp')
    with fs.open('receipt.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'
        return response

    return redirect('orderviews',orderid=orderid)

