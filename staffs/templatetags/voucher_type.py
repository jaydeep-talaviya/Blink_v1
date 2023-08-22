from django import template

register = template.Library()

# @register.simple_tag
@register.filter(name='vouchertype')
def vouchertype(value):
    return " ".join(value.split("_")).title()
