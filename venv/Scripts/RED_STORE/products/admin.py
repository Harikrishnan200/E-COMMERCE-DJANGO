from django.contrib import admin
from django.db import models  # Import the models module
from .models import Product,Category,Size,ProductSize,SubImage
from .models import Size, ProductSize

# Register your models here.

# for auto generation of category_slug field in Category table from category_name fields
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name','category_slug','created_at']
    search_fields = ['category_name','category_slug']
    prepopulated_fields = {'category_slug':('category_name',)}  # this is for auto generation of sulg field from name and this is the corret syntax  {"field_name":'name from where to auto generate'}



# for auto generation of slug field in Product table from model fields
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','model','price','discount_in_percentage','actual_price','total_price','stock','delete_status','is_available','created_at']
    list_filter = ['delete_status','is_available','created_at','updated_at']
    search_fields = ['title','model','price','discount_price','description','priority']
    prepopulated_fields = {'slug':('title',)}
    # prepopulated_fields = {'slug':('title','model')}  # this is for auto generation of sulg field from model and this is the corret syntax  {"field_name":'name from where to auto generate'}
                                                      # for generating the slug field like this shirt-x001   where shirt is the title and x001 is the model


# admin.py


class SizeAdmin(admin.ModelAdmin):
    list_display = ['size', 'created_at', 'updated_at']

admin.site.register(Size, SizeAdmin)

class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['product', 'get_model', 'size', 'quantity', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']

    def get_model(self, obj):
        return obj.product.model

    get_model.short_description = 'Model'  # short_description: Defines a user-friendly name for the column header in the Django admin interface.

admin.site.register(ProductSize, ProductSizeAdmin)


# list_display: Updated to include 'get_model', which is a method that retrieves the model of the product associated with each ProductSize.
# get_model Method: Defined within ProductSizeAdmin, it accesses obj.product.model to fetch the model field of the related Product. The obj here represents each instance of ProductSize in the queryset.

# get_model: This method retrieves the model attribute from the related product object. The obj parameter represents the current instance of ProductSize being processed in the admin interface.
# obj.product.model: Accesses the model attribute of the product related to the ProductSize instance.

# short_description: Provides a human-readable name for the column in the admin interface. In this case, it labels the column as "Model".




admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(SubImage)

