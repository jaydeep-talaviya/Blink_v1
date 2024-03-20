from django import template
from ast import literal_eval
from django.utils.translation import gettext_lazy as _

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key, None) if dictionary and key in dictionary else key

@register.filter(name='get_changed_fields')
def get_changed_fields(changed_fields):
    if changed_fields != 'null':
        return dict(literal_eval(changed_fields))
    else:
        return {}

@register.filter(name='get_event_type')
def get_event_type(event_type):
    TYPES = (
        (1, 'Create'),
        (2, 'Update'),
        (3, 'Delete'),
        (4, 'Many-to-Many Change'),
        (5, 'Reverse Many-to-Many Change'),
        (6, 'Many-to-Many Add'),
        (7, 'Reverse Many-to-Many Add'),
        (8, 'Many-to-Many Remove'),
        (9, 'Reverse Many-to-Many Remove'),
        (10, 'Many-to-Many Clear'),
        (11, 'Reverse Many-to-Many Clear'),
    )
    return list(filter(lambda x: x[0] == event_type, TYPES))[0][1]


