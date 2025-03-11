from django import template

register = template.Library()

# @register.filter
# def times(number):
#     """
#     Returns a range object from 0 to the given number (exclusive).
#     Used in templates to generate loops.
#     """
#     return range(number)


@register.filter
def range_filter(value):
    return range(int(value))