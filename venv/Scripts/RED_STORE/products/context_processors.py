from .models import Category

def menu_links(request):
    category_links = Category.objects.all()
    return {'category_links': category_links}
