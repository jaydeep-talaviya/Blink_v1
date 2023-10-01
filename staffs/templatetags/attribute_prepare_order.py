from django import template

from products.models import OrderLines

register = template.Library()


@register.filter(name='get_price_from_prepare_order')
def get_price_from_prepare_order(record):
    orderline=OrderLines.objects.filter(order_id=record.order_id, product_id=record.stock_id.product_id, qty=record.purchase_qty,
                              selected_product_varient=",".join(
                                  record.stock_id.product_attributes.attribute_values.values_list('a_value',flat=True)) + ',')
    return orderline.first()