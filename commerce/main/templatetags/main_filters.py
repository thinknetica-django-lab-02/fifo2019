from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
@stringfilter
def inverted(value):
    value = list(value)
    value.reverse()
    return ''.join(value)