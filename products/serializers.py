from rest_framework import serializers
# from cart.serializers import CartItemSerializer, CartSerializer
from products.models import Category, Product, ProductImage
from django.utils.text import slugify

class CategorySerializer(serializers.ModelSerializer):       
    class Meta:
        model = Category
        fields =['title', 'description', 'slug']  
        required = True    
  

class ProductImageSerializer(serializers.ModelSerializer): 
    # products =ProductSerializer(many=True, read_only=True)    
    class Meta:
        model = ProductImage
        fields = ['id', 'image1', 'image2'] 

class ProductSerializer(serializers.ModelSerializer):  
    category =serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())    
    images = ProductImageSerializer(many=True, read_only=True)  
    class Meta:
        model = Product
        fields =['category', 'name', 'description', 'price', 'quantity', 'size_variant', 'color_variant', 'slug', 'images'] 
    category = CategorySerializer         

         
class ProductCategorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)  
    class Meta:
        model = Category
        fields =['id', 'title', 'description', 'slug', 'product']  
        required = True         

     