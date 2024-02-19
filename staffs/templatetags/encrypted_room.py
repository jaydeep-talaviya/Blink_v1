from django import template
import hashlib

register = template.Library()

@register.filter
def encrypt_value(user):
    value = str(user.username)+"_"+str(user.id)
    print(">>>>>>>>>value1111",value)
    combined_string = value.encode('utf-8')
    hashed_value = hashlib.sha256(combined_string).hexdigest()
    return hashed_value
