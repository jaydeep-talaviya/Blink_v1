import hashlib

from django.core.mail import EmailMessage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.loader import get_template
from django.conf import settings
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

def send_email_with_template(username, email):
    """Sends an email to the specified user with an HTML template.

    Args:
    username: The username of the user to send the email to.
    email: The email address of the user to send the email to.
    """

    template = get_template('emails/email_template.html')
    context = {
    'username': username,
    'CUSTOMER_SUPPORT_EMAIL':settings.CUSTOMER_SUPPORT_EMAIL
    }
    message = template.render(context)

    email_message = EmailMessage(
    subject='Welcome to Django!',
    body=message,
    from_email=settings.EMAIL_HOST_USER,
    to=[email],
    )
    email_message.content_subtype = 'html'
    email_message.send()


def send_employee_join_email(request,user):
    """Sends an email to the specified user with an HTML template.

    Args:
    username: The username of the user to send the email to.
    email: The email address of the user to send the email to.
    """
    protocol = 'https' if request.is_secure() else 'http'
    domain = request.get_host()
    print(">>>step 1",protocol,domain)

    template = get_template('passwordreset/password_reset_email.html')
    context = {
    'username': user.username,
    'CUSTOMER_SUPPORT_EMAIL':settings.CUSTOMER_SUPPORT_EMAIL,
    'user': user,
    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    'token': default_token_generator.make_token(user),
    'protocol': protocol,
    'domain': domain,
    }
    message = template.render(context)

    email_message = EmailMessage(
    subject='Welcome to The Wooden!',
    body=message,
    from_email=settings.EMAIL_HOST_USER,
    to=[user.email],
    )
    email_message.content_subtype = 'html'
    email_message.send()


def notify_to_warehouser_owner_email(request,user):
    """Sends an email to the specified user with an HTML template.

    Args:
    username: The username of the user to send the email to.
    email: The email address of the user to send the email to.
    """
    protocol = 'https' if request.is_secure() else 'http'
    domain = request.get_host()

    template = get_template('emails/welcome_warehouser_owner.html')
    context = {
    'username': user.username,
    'CUSTOMER_SUPPORT_EMAIL':settings.CUSTOMER_SUPPORT_EMAIL,
    'user': user,
    'protocol': protocol,
    'domain': domain,
    }
    message = template.render(context)

    email_message = EmailMessage(
    subject='Welcome to The Wooden!',
    body=message,
    from_email=settings.EMAIL_HOST_USER,
    to=[user.email],
    )
    email_message.content_subtype = 'html'
    email_message.send()

def get_voucher_discount(voucher,user,user_cart_total_sum):
    discount_amount=0
    if voucher.voucher_type == 'on_above_purchase':
        if voucher.on_above_purchase < user_cart_total_sum:
            discount_amount=voucher.off_price
            print(">>>>>>on_above_purchase",discount_amount)
    elif voucher.voucher_type == 'product_together':
        if all(list(map(lambda x: x in list(user.cart_set.values_list('product_id', flat=True)),
                     list(voucher.products.values_list('id', flat=True)) + [voucher.with_product_id]))):
            discount_amount = voucher.off_price
            print(">>>>>>product_together",discount_amount)

    elif voucher.voucher_type == 'promocode':
        discount_amount = voucher.off_price
        print(">>>>>>promocode", discount_amount)

    return discount_amount


def get_attribute_full_name(orderline):
    return ' with '.join(["-".join(attr) for attr in orderline.product_id.productchangepriceattributes_set.filter(
        attribute_values__a_value__in=orderline.selected_product_varient.split(',')[:-1]).values_list(
        'attribute_values__a_name__a_name', 'attribute_values__a_value').distinct()])


def get_warehouse_dict(orderline):
    queryset = orderline.product_id.stocks_set.all().values('warehouse_id', 'warehouse_id__name').distinct()
    return [{'warehouse_name':item['warehouse_id__name'],'id': item['warehouse_id']} for item in queryset]




def get_orders_count_by_date(models,start_date, end_date):
    # Get the current date
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

    # Initialize a dictionary to store the count for each date
    orders = models[0]
    orderprepare = models[1]
    expenses = models[2]
    payment = models[3]
    delivery = models[4]

    orders_count_by_date = {}
    orderprepare_count_by_date={}
    expenses_credit_count_by_date ={}
    expenses_debit_count_by_date ={}
    payment_by_date ={}
    delivery_confirm_by_date ={}
    delivery_delivering_by_date ={}
    delivery_shipped_by_date ={}

    # Query the database for each date and count the orders
    for date in date_range:
        start_datetime = datetime.combine(date, datetime.min.time())
        end_datetime = datetime.combine(date, datetime.max.time())

        orders_count = orders.objects.filter(created_at__range=(start_datetime, end_datetime),order_status__in=['order_prepared','order_confirm','order_delivering','order_shipped']).count()
        orders_count_by_date[date.strftime('%Y-%m-%d')] = orders_count
        orderprepare_count = orderprepare.objects.filter(created_at__range=(start_datetime, end_datetime)).count()
        orderprepare_count_by_date[date.strftime('%Y-%m-%d')] = orderprepare_count
        # expenses
        ledger_expenses = expenses.objects.filter(creation_date__range=(start_datetime, end_datetime))
        expenses_credit_count_by_date[date.strftime('%Y-%m-%d')] = sum([expense.get_total_ledger_credit() for expense in ledger_expenses])
        expenses_debit_count_by_date[date.strftime('%Y-%m-%d')] = sum([expense.get_total_ledger_debit() for expense in ledger_expenses])
        # payment
        payments = payment.objects.filter(created_at__range=(start_datetime, end_datetime),status__in=['SUCCESS'])
        payment_by_date[date.strftime('%Y-%m-%d')] = sum(payments.values_list('order_id__amount',flat=True))
        # deliveries
        confirm_deliveries = delivery.objects.filter(created_at__range=(start_datetime, end_datetime),state='Confirm')
        delivering_deliveries = delivery.objects.filter(updated_at__range=(start_datetime, end_datetime),state='Delivering')
        shipped_deliveries = delivery.objects.filter(delivered_at__range=(start_datetime, end_datetime),state='Shipped')
        delivery_confirm_by_date[date.strftime('%Y-%m-%d')] = confirm_deliveries.count()
        delivery_delivering_by_date[date.strftime('%Y-%m-%d')] = delivering_deliveries.count()
        delivery_shipped_by_date[date.strftime('%Y-%m-%d')] = shipped_deliveries.count()

    return orders_count_by_date,orderprepare_count_by_date,expenses_credit_count_by_date,expenses_debit_count_by_date,payment_by_date,delivery_confirm_by_date,delivery_delivering_by_date,delivery_shipped_by_date


def get_pagination_records(request,records):
    # Number of categories to display per page
    per_page = 10  # Adjust as needed
    # Paginate the categories
    paginator = Paginator(records, per_page)
    page = request.GET.get('page')

    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, deliver the first page
        records = paginator.page(1)
    except EmptyPage:
        # If the page is out of range (e.g., 9999), deliver the last page
        records = paginator.page(paginator.num_pages)
    return records


def get_paginator(paginator,page):
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)
    return records

def encrypt_value(value):
    # Combine username and id into a single string
    combined_string = value.encode('utf-8')

    # Use SHA-256 for hashing
    hashed_value = hashlib.sha256(combined_string).hexdigest()

    return hashed_value

def get_related_url(request,purpose,id=None):
    base_url = request.build_absolute_uri(reverse('dashboard'))
    if purpose == 'warehouse':
        base_url = request.build_absolute_uri(reverse('list_warehouses'))
    if purpose == 'stock':
        base_url = request.build_absolute_uri(reverse('stock_list'))
        if id:
            base_url = request.build_absolute_uri(reverse('stock_update',kwargs={'id':id}))
    if purpose == 'product':
        base_url = request.build_absolute_uri(reverse('product_list'))
        if id:
            base_url = request.build_absolute_uri(reverse('product_update',kwargs={'id':id}))
    if purpose == 'order':
        base_url = request.build_absolute_uri(reverse('orderlists'))
        if id:
            base_url = request.build_absolute_uri(reverse('orderlists_with_status',kwargs={'status':'order_cancel'}))
    if purpose == 'delivery':
        base_url = request.build_absolute_uri(reverse('delivery_list'))
        if id:
            base_url = request.build_absolute_uri(reverse('orderlists_with_status',kwargs={'status':'order_shipped'}))
    if purpose == 'product_qa':
        base_url = request.build_absolute_uri(reverse('product_list_with_type',kwargs={'type':'in_qa'}))
    return base_url

def send_mail_to_all_managers(creater_manager,managers_emails):
    template = get_template('emails/notify_to_all_manager.html')
    context = {
        'creater_manager': creater_manager,
    }
    message = template.render(context)

    email_message = EmailMessage(
        subject='Welcome to Django!',
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=managers_emails,
    )
    email_message.content_subtype = 'html'
    email_message.send()


def send_mail_to_delivery_person(delivery_person,prepared_orders):
    template = get_template('emails/notify_delivery_person.html')
    context = {
        'prepared_orders': prepared_orders,
        'delivery_person':delivery_person
    }
    message = template.render(context)

    email_message = EmailMessage(
        subject='Notification to Pick up Delivery',
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[delivery_person.email],
    )
    email_message.content_subtype = 'html'
    email_message.send()

def send_email_to_notify_customer(customer,prepared_orders):
    template = get_template('emails/notify_customer_to_delivery.html')
    context = {
        'customer': customer,
        'prepared_orders': prepared_orders,

    }
    message = template.render(context)

    email_message = EmailMessage(
        subject='Notification to Pick up Delivery',
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[delivery_person.email],
    )
    email_message.content_subtype = 'html'
    email_message.send()
