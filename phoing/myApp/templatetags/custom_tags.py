from django import template

register = template.Library()


@register.filter
def get_at_index(list, index):
    if len(list) > index:
        return list[index]
    else:
        return False
