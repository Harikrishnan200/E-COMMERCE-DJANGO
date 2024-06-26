from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'layout.html')

def product(request):
    return render(request,'product_page_content.html')

def detail_product(request):
    return render(request,'product_details.html')

def cart(request):
    return render(request,'cart.html')

def account(request):
    return render(request,'account.html')