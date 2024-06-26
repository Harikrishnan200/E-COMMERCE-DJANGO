from django.contrib import admin
from django.db import models  # Import the models module
from .models import Product,Category
# Register your models here.

# for auto generation of category_slug field in Category table from category_name fields
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name','category_slug','created_at']
    search_fields = ['category_name','category_slug']
    prepopulated_fields = {'category_slug':('category_name',)}  # this is for auto generation of sulg field from name and this is the corret syntax  {"field_name":'name from where to auto generate'}



# for auto generation of slug field in Product table from model fields
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','model','price','discount_price','delete_status','is_available','created_at']
    list_filter = ['delete_status','is_available','created_at','updated_at']
    search_fields = ['title','model','price','discount_price','description','priority']
    prepopulated_fields = {'slug':('title','model')}  # this is for auto generation of sulg field from model and this is the corret syntax  {"field_name":'name from where to auto generate'}
                                                      # for generating the slug field like this shirt-x001   where shirt is the title and x001 is the model


admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)