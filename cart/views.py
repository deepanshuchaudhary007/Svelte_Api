import datetime
import json
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cart, CartItem
from cart.serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, ProductItemSerializer, UserCartItems, UserCartSerializer
from products.models import Product
from users.models import User
from users.serializers import UserSerializer

# Create your views here.
@api_view(['POST'])
def add_to_cart(request):
    try:
        message = "Product Add Successfully"
        data = request.data
        print(data)                
        if data:             
            serializer = AddCartItemSerializer(data=data, many=False) 
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
def user_cart(request, user_code):
    try:        
        message = "User Details"
        user = User.objects.filter(user_code=user_code)        
        if user is None:
            message = "No product were found"
            return Response({"message": message}, status=404)
        serializer = UserCartSerializer(user, many=True)
        print(serializer.data)        
        return Response({"message": message, "data":serializer.data}, status=200)
    except Exception as e:
        print(str(e))
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500) 

@api_view(['GET'])
def user_cart_items(request, id):
    try:        
        message = "User Cart Details"
        cart = Cart.objects.filter(id=id)        
        if cart is None:
            message = "No product were found"
            return Response({"message": message}, status=404)
        serializer = CartSerializer(cart, many=True)
        data = serializer.data
        print(data)
        return Response({"message": message, "data":serializer.data}, status=200)
    except Exception as e:
        print(str(e))
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500)
          
@api_view(['DELETE'])
def delete_cart_item(request, id):
    try:
        message = " Cart item deleted successfully"
        cart_item = CartItem.objects.get(id=int(id))
        print(cart_item)
        if cart_item is None:
            message = "Product not found in cart"
            return Response({"message": message}, status=404)    
        cart_item.delete()
        return Response({"message": message}, status=404)
    except Exception as e:
        print(str(e))
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500) 



















@api_view(['GET'])
def cart_items(request, id):    
    try:
        message = "Cart Details"
        cart = Cart.objects.filter(id=id)
        if cart is None:
            message = "No product were found"
            return Response({"message": message}, status=404)
        serializer = ProductCartItemSerializer(cart, many=True)        
        return Response({"message": message, "data":serializer.data}, status=200)
    except Exception as e:
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500)    
    



@api_view(['PUT', 'PATCH'])
def update_cart(request, id):
    try:
        message="Product updated successfully"
        cart = CartItem.objects.filter(id=id)
        data = request.data  
        if data: 
            print("inside category update") 
            if cart is None:
                message="Category not found"
                return Response({"message":message}, status=404)
            if request.method == "PUT":   
                serializer = CartItemSerializer(instance=cart, data=data)                 
                try:                    
                    if serializer.is_valid():
                        serializer.save()                        
                    return Response({"data":serializer.data, "message":message}, status=200)
                except Exception as e:
                    print(str(e)) 
                    return Response({"message":"Something went worng, please try later"}, status=500)                        
            elif request.method == "PATCH":
                serializer = CartItemSerializer(instance=cart, data=data, partial=True)                               
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
    




# def cart(self, request, pk):
#     item = get_object_or_404(Product, pk=pk)
#     order_item, created = CartItem.objects.get_or_create(
#         item=item,
#         user=self.request.user,
#         ordered=False
#     )
#     order_qs = Cart.objects.filter(user=self.request.user, ordered=False)

#     if order_qs.exists():
#         order = order_qs[0]

#         if order.items.filter(item__pk=item.pk).exists():
#             order_item.quantity += 1
#             order_item.save()
#             return Response({"message": "Quantity is added",
#                                 },
#                             status=200
#                             )
#         else:
#             order.items.add(order_item)
#             return Response({"message": " Item added to your cart", },
#                             status=200
#                             )
#     else:
#         ordered_date = datetime.now()
#         order = Cart.objects.create(user=self.request.user, ordered_date=ordered_date)
#         order.items.add(order_item)
#         return Response({"message": "Order is created & Item added to your cart", },
#                         status=200
#                         )
