from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderedItem
from customer.models import Customer
from products.models import Product, ProductSize, Size
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Declare the global variable
global_quantity = 0

@login_required(login_url='account')
def set_global_quantity(quantity):   
    global global_quantity
    global_quantity = quantity


 # To retrieve the global quantity value in remove_item fn
@login_required(login_url='account')
def get_global_quantity():   
    return global_quantity


@login_required(login_url='account')
def show_cart(request):
    user = request.user
    customer = user.customer_profile
    cart_obj, created = Order.objects.get_or_create(
        owner=customer,
        order_status=Order.CART_STAGE
    )
    
    context = {
        'cart_obj': cart_obj
    }
    return render(request, 'cart.html', context)


@login_required(login_url='account')
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        if hasattr(user, 'customer_profile'):
            customer = user.customer_profile
        else:
            return HttpResponse("User does not have a customer profile.", status=400)

        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        size_value = request.POST.get('size')
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if not provided or invalid

        if quantity <= 0:
            messages.info(request, "Invalid quantity.")
            return redirect(reverse('detail_product', kwargs={'pk': product_id}))

        try:
            size = Size.objects.get(size=size_value)
            product_size = ProductSize.objects.get(
                product=product,
                size=size
            )
        except (Size.DoesNotExist, ProductSize.DoesNotExist):
            product_size = None

        if product.stock == 0:
            messages.info(request, "Product is out of stock.")
            return redirect(reverse('detail_product', kwargs={'pk': product_id}))
        elif product.stock < quantity:
            messages.info(request, "Not enough stock for this product.")
            return redirect(reverse('detail_product', kwargs={'pk': product_id}))

        cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )

        ordered_item, created = OrderedItem.objects.get_or_create(
            product=product,
            size=product_size,
            owner=cart_obj,
            defaults={'quantity': quantity}
        )

        if not created:
            ordered_item.quantity += quantity
            ordered_item.save()

        # Update stock
        product.stock -= quantity
        product.save()

        # Set the global quantity
        set_global_quantity(quantity)

        return redirect('cart')

    return render(request, 'cart.html')

@login_required(login_url='account')
def remove_item(request, pk):
    try:
        item = OrderedItem.objects.get(id=pk)
        product = item.product

        # Update stock using the global quantity
        global_quantity = get_global_quantity()
        product.stock += global_quantity
        product.save()

        item.delete()

    except OrderedItem.DoesNotExist:
        return HttpResponse(f"OrderedItem with pk {pk} does not exist", status=404)

    return redirect('cart')

@login_required(login_url='account')
def order_confirmed(request):
    user = request.user
    customer = user.customer_profile
    cart_obj = Order.objects.get(owner=customer, order_status=Order.CART_STAGE)
    # for item in cart_obj.added_carts.all():
    #     print(item.product.title)
    cart_obj.order_status = Order.ORDER_CONFIRMED
    cart_obj.save()

    return redirect('cart')


@login_required(login_url='account')
def view_orders(request):
    user = request.user
    customer = user.customer_profile
    orders = Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)

    # Create a list of ordered items for each order
    order_items = OrderedItem.objects.filter(owner__in=orders)

    context = {
        'orders': orders,
        'order_items': order_items
    }

    return render(request, 'orders.html', context)