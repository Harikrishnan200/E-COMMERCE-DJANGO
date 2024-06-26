from django.db import models
from customer.models import Customer
# Create your models here.

# for cart objects of a customer. Ushually a customer have more than one cart
class Order(models.Model):
    LIVE = 1
    DELETE = 2
    DELETE_CHOICES = (
                (LIVE, 'Live'),
                (DELETE,'Delete')
            )
    CART_STAGE = 0
    ORDER_CONFIRMED = 1
    ORDER_PROCESSED = 2
    ORDER_DELIVERED = 3
    OREDR_REJECTED = 4
    STATUS_CHOICES = (

        (ORDER_PROCESSED,'Processed'),
        (ORDER_DELIVERED,'Delivered'),
        (OREDR_REJECTED,'Rejected')
    )
    order_status = models.IntegerField(choices=STATUS_CHOICES,default=CART_STAGE)
    owner = models.ForeignKey(Customer,related_name='orders',on_delete=models.SET_NULL,null=True)
    delete_status = models.IntegerField(choices=DELETE_CHOICES,default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# This model is used to specify the details of each cart items like quantity
class OrderedItem(models.Model):
    product = models.ForeignKey('products.Product',related_name='product_items',on_delete=models.CASCADE)  # products.Product defines a foreign key relationship between the model in which this line appears and the Product model located in the products app.
    quantity = models.IntegerField(default=1)
    owner = models.ForeignKey(Order,related_name='added_carts',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title