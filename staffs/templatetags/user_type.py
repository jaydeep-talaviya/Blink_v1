from django import template

register = template.Library()

# @register.simple_tag
@register.filter(name='employee_type')
def employee_type(user):
    print(user,"??????")
    if user.is_superuser:
        return 'admin'
    elif hasattr(user, 'employee'):
        return user.employee.type
    else:
        return ''