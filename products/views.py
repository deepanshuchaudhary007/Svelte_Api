import io
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import Category, Product, ProductImage
from products.serializers import CategorySerializer, ProductCategorySerializer, ProductImageSerializer, ProductSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# Create your views here.
################# Category Logic's Start #################
@api_view(['POST'])
def create_category(request):
    try:
        data =request.data
        if data:        
            serializer = CategorySerializer(data=data, many=False)   
            if serializer.is_valid():
                serializer.save()
            return Response({"message": "Category created successfully"}, status=200)
        return Response({"message":"Nothing were found with request"}, status=400)    
    except Exception as e:
        print(str(e))
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500)           

@api_view(['GET'])
def all_category(request):
    try:
        category = Category.objects.all()
        if category is None:
            message = "No category were found"
            return Response({"message": message}, status=404)
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)
    except Exception as e:
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500)
    
@api_view(['GET'])
def category_details(request, slug=None):
    try:
        message = "Category details"
        category = Category.objects.filter(slug=slug)
        if category is None:
            message = "Category not found"
            return Response({"message": message}, status=404)
        serializer = CategorySerializer(category, many=True)        
        return Response(serializer.data, status=200)
    except Exception as e:
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500)
    
@api_view(['PUT', 'PATCH'])
def category_update(request, slug=None):
    try:
        message="Category updated successfully"
        category = Category.objects.filter(slug=slug).first()
        data = request.data
        if data: 
            print("inside category update") 
            if category is None:
                message="Category not found"
                return Response({"message":message}, status=404)
            if request.method == "PUT":   
                serializer = CategorySerializer(instance=category, data=data)                 
                try:                    
                    if serializer.is_valid():
                        serializer.save()                        
                    return Response({"data":serializer.data, "message":message}, status=200)
                except Exception as e:
                    print(str(e)) 
                    return Response({"message":"Something went worng, please try later"}, status=500)                        
            elif request.method == "PATCH":
                serializer = CategorySerializer(instance=category, data=data, partial=True)                               
                try:                    
                    if serializer.is_valid():
                        serializer.save()                        
                    return Response({"data":serializer.data, "message":message}, status=200)
                except Exception as e:
                    print(str(e)) 
                    return Response({"message":"Something went worng, please try later"}, status=500)                                      
        return Response({"message":"Nothing were found with request"}, status=400)      
    except Exception as e:
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500)
    
@api_view(['DELETE'])
def category_delete(request, slug=None):
    try:
        message = "Category deleted successfully"
        category = Category.objects.filter(slug = slug)    
        if category is None:
            message = "Category not found"
            return Response({"message": message}, status=404)    
        category.delete()
        return Response({"message": message}, status=200)
    except Exception as e:
        print(str(e))
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500) 

################# Category Logic's Ends #################

################# Product Logic's Start #################
@api_view(['POST'])
def create_product(request):
    try:
        message = "Product Successfully Created"
        data =request.data                 
        if data:             
            serializer = ProductSerializer(data=data, many=False) 
            print(serializer.is_valid(raise_exception=True))  
            if serializer.is_valid():
                serializer.save()
                return Response({"message":message}, status=200) 
        return Response({"message":"Nothing were found with request"}, status=400)             
    except Exception as e:
        print(str(e))
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500) 

@api_view(['GET'])
def all_product(request):    
    try:
        message = "Product Details"
        product = Product.objects.all()
        if product is None:
            message = "No product were found"
            return Response({"message": message}, status=404)
        serializer = ProductSerializer(product, many=True)        
        return Response({"message": message, "data":serializer.data}, status=200)
    except Exception as e:
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500)

@api_view(['GET'])
def product_on_category(request, slug=None):    
    try:        
        message = "Product Details"
        category = Category.objects.filter(slug=slug)        
        if category is None:
            message = "No product were found"
            return Response({"message": message}, status=404)
        serializer = ProductCategorySerializer(category, many=True)
        print(serializer)        
        return Response({"message": message, "data":serializer.data}, status=200)
    except Exception as e:
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500)    

    
@api_view(['GET'])
def product_details(request, slug=None):
    try:
        message = "Product Details"
        product = Product.objects.filter(slug=slug)
        if product is None:
            message = "Product not found"
            return Response({"message": message}, status=404)
        serializer = ProductSerializer(product, many=True)
        return Response({"message":message, "data":serializer.data}, status=200)
    except Exception as e:
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500)
    
@api_view(['PUT', 'PATCH'])
def product_update(request, slug=None):
    try:
        message="Product updated successfully"
        product = Product.objects.filter(slug=slug).first()
        data = request.data  
        if data: 
            print("inside category update") 
            if product is None:
                message="Category not found"
                return Response({"message":message}, status=404)
            if request.method == "PUT":   
                serializer = CategorySerializer(instance=product, data=data)                 
                try:                    
                    if serializer.is_valid():
                        serializer.save()                        
                    return Response({"data":serializer.data, "message":message}, status=200)
                except Exception as e:
                    print(str(e)) 
                    return Response({"message":"Something went worng, please try later"}, status=500)                        
            elif request.method == "PATCH":
                serializer = CategorySerializer(instance=product, data=data, partial=True)                               
                try:                    
                    if serializer.is_valid():
                        serializer.save()                        
                    return Response({"data":serializer.data, "message":message}, status=200)
                except Exception as e:
                    print(str(e)) 
                    return Response({"message":"Something went worng, please try later"}, status=500)                                      
        return Response({"message":"Nothing were found with request"}, status=400) 
    except Exception as e:
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500)   
    
@api_view(['DELETE'])
def product_delete(request, slug=None):
    try:
        message = "Product deleted successfully"
        product = Product.objects.filter(slug=slug).first()
        if product is None:
            message = "Product not found"
            return Response({"message": message}, status=404)    
        product.delete()
        return Response({"message": message}, status=404)
    except Exception as e:
        print(str(e))
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500) 
    

################# Product Logic's Ends #################

################# Product Image Logic's Ends #################
@api_view(['POST'])
def add_product_image(request):
    try:
        data =request.data
        if data:        
            serializer = ProductImageSerializer(data=data, many=False)    
            if serializer.is_valid():
                serializer.save()
            return Response({"message": "Product image saved successfully"}, status=200)
        return Response({"message":"Nothing were found with request"}, status=400)    
    except Exception as e:
        print(str(e))
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500)   
    
@api_view(['PUT', 'PATCH'])
def update_product_image(request, id=None):    
    try:
        message="Product images updated successfully"
        product_image = ProductImage.objects.filter(id=int(id)).first()
        data = request.data  
        if data: 
            print("inside category update") 
            if product_image is None:
                message="Category not found"
                return Response({"message":message}, status=404)
            if request.method == "PUT":   
                serializer = CategorySerializer(instance=product_image, data=data)                 
                try:                    
                    if serializer.is_valid():
                        serializer.save()                        
                    return Response({"data":serializer.data, "message":message}, status=200)
                except Exception as e:
                    print(str(e)) 
                    return Response({"message":"Something went worng, please try later"}, status=500)                        
            elif request.method == "PATCH":
                serializer = CategorySerializer(instance=product_image, data=data, partial=True)                               
                try:                    
                    if serializer.is_valid():
                        serializer.save()                        
                    return Response({"data":serializer.data, "message":message}, status=200)
                except Exception as e:
                    print(str(e)) 
                    return Response({"message":"Something went worng, please try later"}, status=500)                                      
        return Response({"message":"Nothing were found with request"}, status=400) 
    except Exception as e:
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500)
    
@api_view(['DELETE'])
def delete_product_image(request, id=None):    
    try:
        message = "Product images deleted successfully"
        product_image = ProductImage.objects.filter(id=int(id)).first()
        if product_image is None:
            message = "Product not found"
            return Response({"message": message}, status=404)    
        product_image.delete()
        return Response({"message": message}, status=404)
    except Exception as e:
        print(str(e))
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500)  

################# Product Image Logic's Ends #################