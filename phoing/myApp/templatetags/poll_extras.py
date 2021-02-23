from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def lower(value):
    return value.lower()

@register.filter
@stringfilter
def datefilter(date):
    return date[0:11]