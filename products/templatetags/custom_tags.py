from django import template
from django.db.models import Avg

register = template.Library()

# @register.simple_tag
@register.filter(name='get_avarage_rate')
def get_avarage_rate(value):
    print(value.count(),".....................")
    if value.count() != 0:
        avg_rates=value.aggregate(Avg('rate'))['rate__avg']
        rate_list=['orange' for i in range(int(avg_rates))]+['black' for i in range(5-int(avg_rates))]
        print(rate_list)
        return rate_list
    else:
        return []

@register.filter(name='paymentstype')
def paymentstype(value):
    if value=='order_not_confirm':
        value=" Order Not Confirmed"
    else:
        value=value.split("_")
        value.reverse()
        value=" ".join(value)
    return value
