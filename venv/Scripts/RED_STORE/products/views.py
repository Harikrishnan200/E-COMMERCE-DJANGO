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

def list_product(request):
    page = 1

    if 'page' in request.GET:
        page = request.GET.get('page')

    # products = Product.objects.all()
    products = Product.objects.order_by('-priority')   # To fetech the products with higher priority
    paginator = Paginator(products, 3)
    products = paginator.get_page(page)
    context = {
        'products': products
    }
    return render(request,'product_page_content.html',context)

def detail_product(request,pk=None):
    sub_images = None
    product = Product.objects.get(id=pk)
    sub_images = SubImage.objects.filter(product=product)   # To filter the sub images of the product
    sizes = ProductSize.objects.filter(product=product)
 
    context = {
        'product': product,
        'sub_images': sub_images,
        'sizes': sizes
    }
    return render(request,'product_details.html',context)


