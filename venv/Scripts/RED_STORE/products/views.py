from django.shortcuts import render,redirect
from .models import Product,SubImage,ProductSize
from django.core.paginator import Paginator
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    featured_products = Product.objects.order_by('-priority')[:4]  # To fetch firts 4 products with higher priority (decenting order)
    latest_products = Product.objects.order_by('-id')[:4]    # To fetch firts 4 last added products (ie the products with higher id)
    
    context = {
        'featured_products': featured_products,
        'latest_products': latest_products
    }
    return render(request,'layout.html',context)   
#The context dictionary you create in the index view function, containing the keys 
# 'featured_products' and 'latest_products', is passed to the layout.html template when rendering. These keys, and their associated 
# values, will be available only within the scope of that specific template rendering. If layout.html includes other templates or if it
# extends from a base template, those keys will also be available in those included or extended templates during that rendering process.

def list_product(request,sort_slug=None):

    page = 1

    if 'page' in request.GET:
        page = request.GET.get('page')

    if sort_slug is not None:
        products = Product.objects.all().filter(slug=sort_slug).order_by('-priority')
        if products:
            paginator = Paginator(products, 8)
            products = paginator.get_page(page)
        else:
            products = None    
        context = {
            'products': products
        }
        return render(request,'product_page_content.html',context)   
        
        
    # products = Product.objects.all()
    products = Product.objects.order_by('-priority')   # To fetech the products with higher priority
    paginator = Paginator(products, 8)
    products = paginator.get_page(page)
    context = {
        'products': products
    }
    return render(request,'product_page_content.html',context)


def detail_product(request,pk=None,product_slug=None):
    sub_images = None
    product = Product.objects.get(id=pk)
    sub_images = SubImage.objects.filter(product=product)   # To filter the sub images of the product
    sizes = ProductSize.objects.filter(product=product)

    related_products = Product.objects.all().filter(slug = product_slug).filter(is_available = True)
    print(product_slug)
    print(related_products)

    if product.stock == 0:
        message = "Out of Stock"
    elif product.stock <= 5:
        message = f"Only {product.stock} items left."
    elif product.stock <=10:    
        message = "Only few left."
    else:
        message = None

 
    context = {
        'product': product,
        'sub_images': sub_images,
        'sizes': sizes,
        'few_item_message': message,
        'related_products': related_products
    }
    return render(request,'product_details.html',context)


# def sort_products(request,sort_slug=None):
#     products = Product.objects.all().filter(slug=sort_slug)
#     print(products)
#     context = {
#         'sorted_products': products
#     }
#     return render(request,'product_page_content.html',context)

