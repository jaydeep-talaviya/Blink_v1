from django import template

from utils.helper_functions import get_attribute_full_name, get_warehouse_dict

register = template.Library()


@register.filter(name='get_attribute_from_orderline')
def get_attribute_from_orderline(record):
    return get_attribute_full_name(record)


@register.filter(name='get_attribute_id_from_orderline')
def get_attribute_id_from_orderline(record):
    # List of attribute values you want to filter with
    attribute_values_list = record.selected_product_varient.split(',')[:-1]
    # Initialize a list to hold the querysets for each attribute value
    querysets = []

    # Create a queryset for each attribute value
    for attr_value in attribute_values_list:
        queryset = record.product_id.productchangepriceattributes_set.filter(attribute_values__a_value=attr_value)
        querysets.append(queryset)

    # Find the intersection of the querysets
    filtered_records = querysets[0]
    for queryset in querysets[1:]:
        filtered_records = filtered_records.intersection(queryset)
    print(">>>>>>>>>>intersection\n\n\n\n",filtered_records)
    return filtered_records.first().id

@register.filter(name='get_left_qty_in_warehouse_for_product')
def get_left_qty_in_warehouse_for_product(orderline,warehouse):
    product_attribute =get_attribute_id_from_orderline(orderline)
    stocks = orderline.product_id.stocks_set.filter(warehouse_id_id=warehouse.get('id'), product_attributes=product_attribute,
                                           finished=False)
    return stocks.first()

@register.filter(name='get_warehouse_from_orderline')
def get_warehouse_from_orderline(record):
    return get_warehouse_dict(record)

