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
    

    
class Product(models.Model):
    LIVE = 1
    DELETE = 2
    DELETE_CHOICES = (
                (LIVE, 'Live'),
                (DELETE,'Delete')
            )
    title = models.CharField(max_length=200)
    model = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category')
    price = models.FloatField()
    discount_price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='media')
    priority = models.IntegerField(default=0)
    delete_status = models.IntegerField(choices=DELETE_CHOICES,default=LIVE)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

    

