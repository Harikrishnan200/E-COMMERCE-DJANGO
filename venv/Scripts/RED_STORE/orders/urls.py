from django.urls import path
from . import views

urlpatterns = [
    path('cart/',views.show_cart, name='cart'),
   path('add_to_cart/',views.add_to_cart, name='add_to_cart'),
   path('remove_item/<int:pk>',views.remove_item, name='remove_item'),
   path('orders/',views.view_orders, name='orders'),
   path('order_confirmed/',views.order_confirmed, name='order_confirmed'),
]