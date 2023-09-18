from django import template

from utils.helper_functions import get_attribute_full_name

register = template.Library()


@register.filter(name='get_attribute_from_orderline')
def get_attribute_from_orderline(record):
    return get_attribute_full_name(record)
