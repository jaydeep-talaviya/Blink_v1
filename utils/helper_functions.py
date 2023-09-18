from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.conf import settings


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
