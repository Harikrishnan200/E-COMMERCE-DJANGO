from django import template

register = template.Library()

@register.simple_tag(name='multiply')
def chunks(a, b):
    return a*b      


 