from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.conf import settings
from datetime import datetime, timedelta


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