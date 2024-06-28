from django import template

register = template.Library()

@register.simple_tag(name='get_total_price')
def get_total_price(cart_obj):
    total = 0
    for item in cart_obj.added_carts.all():
        total += item.quantity * item.product.price    
    return total