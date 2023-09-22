from django import template

from utils.helper_functions import get_attribute_full_name

register = template.Library()


@register.filter(name='get_product_attributes')
def get_product_attributes(product_attributes):
    return ' with '.join([str(product_attribute) for product_attribute in product_attributes])


