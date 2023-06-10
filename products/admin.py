from django.contrib import admin
from products.models import ProductImage, Category, Product

# Register your models here.
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(Product)