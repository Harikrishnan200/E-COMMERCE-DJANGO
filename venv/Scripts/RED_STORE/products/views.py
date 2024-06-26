from django.shortcuts import render
from .models import Product
# Create your views here.

def index(request):
    return render(request,'layout.html')

def list_product(request):
    products = Product.objects.all()
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