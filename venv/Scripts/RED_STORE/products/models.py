from django.db import models

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    category_slug = models.SlugField(max_length=50,unique=True)
    category_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name
    

    
from django.db import models

class Product(models.Model):
    LIVE = 1
    DELETE = 2
    DELETE_CHOICES = (
        (LIVE, 'Live'),
        (DELETE, 'Delete')
    )
    
    title = models.CharField(max_length=200)
    model = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200)  # unique = True avoided
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    price = models.FloatField()
    actual_price = models.FloatField(default=0.0)
    discount_in_percentage = models.PositiveIntegerField(default=0)
    total_price = models.FloatField(default=0.0)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    priority = models.IntegerField(default=0)
    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
       
        self.actual_price = self.price
        self.discount_in_percentage  = self.discount_in_percentage 
        # Calculate total_price based on price and discount_price
        self.total_price = self.price - (self.price * self.discount_in_percentage /100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.model}"

    
class SubImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sub_images')
    image = models.ImageField(upload_to='product_images/sub_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title} - {self.product.model} - SubImage {self.id}"

class Size(models.Model):
    XS = 1
    S = 2
    M = 3
    L = 4
    XL = 5
    XXL = 6
    SIZE_CHOICES = (
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large')
    )

    size = models.CharField(max_length=3, choices=SIZE_CHOICES, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.size

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_sizes')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='product_sizes')
    quantity = models.PositiveIntegerField(default=0)  # Quantity available for this size
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'size')

    def __str__(self):
        return f"{self.product.title} - {self.product.model} - Size {self.size.size}"
