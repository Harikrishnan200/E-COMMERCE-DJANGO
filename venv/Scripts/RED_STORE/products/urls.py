from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('product/', views.product, name='product'),
    path('product_detail_content/', views.detail_product, name='detail_product'),
    path('cart_page/', views.cart, name='cart_page'),
    path('account/', views.account, name='account'),
]
