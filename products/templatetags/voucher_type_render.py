# Import template module
from django import template
# Create an object of Library()
register = template.Library()
# Define the template file for the inclusion tag
@register.inclusion_tag('voucher_type_render.html')
def voucher_type_render(voucher):
    # Declare a empty list
    print(">>>>>>\n\n\n\n\n\n\n\n\n\n\n\n",voucher)
    return {"voucher":voucher}