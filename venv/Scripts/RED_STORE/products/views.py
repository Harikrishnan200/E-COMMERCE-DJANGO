from django.shortcuts import render
from .models import Product
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    return render(request,'layout.html')

def list_product(request):
    page = 1
    
    if 'page' in request.GET:
        page = request.GET.get('page')

    products = Product.objects.all()
    paginator = Paginator(products, 3)
    products = paginator.get_page(page)
    context = {
        'products': products
    }
    return render(request,'product_page_content.html',context)

def detail_product(request):
    return render(request,'product_details.html')

def cart(request):
    return render(request,'cart.html')

def account(request):
    return render(request,'account.html')