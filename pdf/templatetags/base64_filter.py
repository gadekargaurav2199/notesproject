import base64
from django import template

register = template.Library()

@register.filter(name='base64')
def base64_filter(value):
    if isinstance(value, bytes):
        return base64.b64encode(value).decode('utf-8')
    return value
