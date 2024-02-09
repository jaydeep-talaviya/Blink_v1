from django import template

register = template.Library()

@register.simple_tag(name='deals_of_day_price')
def deals_of_day_price(original_value,percent_off):
    percent_off = 0 if not percent_off else percent_off
    value= float(original_value)-(float(original_value)*float(percent_off))/100
    return value
