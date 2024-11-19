# blog/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def split(value, key):
    """
    Splits the string based on the `key` and returns a list.
    Usage: {{ value|split:":" }}
    """
    return value.split(key)

# blog/templatetags/custom_filters.py

# from django import template

# register = template.Library()

# @register.filter
# def split_string(value, delimiter):
#     return value.split(delimiter) if value else []
