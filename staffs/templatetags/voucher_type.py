from django import template

register = template.Library()

# @register.simple_tag
@register.filter(name='vouchertype')
def vouchertype(value):
    return " ".join(value.split("_")).title()


@register.filter(name='voucher_multiple_records_value')
def voucher_multiple_records_value(records):
    return ",".join([str(record) for record in records])
