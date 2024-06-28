from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.list_product, name='products'),
    path('product_detail/<int:pk>/', views.detail_product, name='detail_product'),
    

]
