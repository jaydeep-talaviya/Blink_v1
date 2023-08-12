# from celery import shared_task
from .models import Cart
from ecommerce_blink.celery import app
from celery import shared_task 
from .models import Orders

@shared_task 
def remove_all_cart_products():
    """
    Saves latest image from Flickr
    """
    all_carts=Cart.objects.all().delete()
    orders=Orders.objects.filter(order_status='order_confirm')
    orders.update(order_status='order_cancel')
    # logger.info(f"All Carts Are Removed Successfully ")
    print('All Carts Are Removed Successfully and Order cancel')