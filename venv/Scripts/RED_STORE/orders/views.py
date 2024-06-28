from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderedItem
from customer.models import Customer
from products.models import Product, ProductSize, Size
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse


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

def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        if hasattr(user, 'customer_profile'):   # hasattr() function: This built-in Python function checks if an object has a specific attribute. It returns True if the attribute exists and False otherwise.
            customer = user.customer_profile
        else:
            return HttpResponse("User does not have a customer profile.", status=400)

        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        size_value = request.POST.get('size')
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if not provided or invalid

        

        # Validate and get ProductSize
        try:
            size = Size.objects.get(size=size_value)
            product_size = ProductSize.objects.get(
                product=product,
                size=size
            )
        except (Size.DoesNotExist, ProductSize.DoesNotExist):
            product_size = None

        if product.stock < quantity:
            messages.info(request, "Not enough stock for this product.")
            # Generate the URL for the product detail view
            return redirect(reverse('detail_product', kwargs={'pk': int(product_id)}))  # pk is used because pk is the url parameter used in the url
        

        # Create or get the order (cart)
        cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )

        # Try to find existing OrderedItem or create a new one
        try:
            ordered_item = OrderedItem.objects.filter(
                product=product,
                size=product_size,
                owner=cart_obj
            ).first()  # To handle if multiple objects are present

            if ordered_item:
                ordered_item.quantity += quantity
                ordered_item.save()
            else:
                ordered_item = OrderedItem.objects.create(
                    product=product,
                    quantity=quantity,
                    size=product_size,
                    owner=cart_obj
                )
            # Update stock
            product.stock -= quantity
            product.save()    

        except OrderedItem.MultipleObjectsReturned:
            # Handle case where multiple OrderedItem instances exist (optional)
            pass

        return redirect('cart')

    return render(request, 'cart.html')

def remove_item(request, pk):
    
    try:
        item = OrderedItem.objects.get(id=pk)
        item.delete()
    except OrderedItem.DoesNotExist:
        print(f"OrderedItem with pk {pk} does not exist")
        return HttpResponse(f"OrderedItem with pk {pk} does not exist", status=404)
    return redirect('cart')


