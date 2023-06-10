import uuid
from rest_framework import serializers
from cart.models import Cart, CartItem
from products.models import Product
from products.serializers import ProductSerializer
from users.models import User
from users.serializers import UserSerializer

class ProductItemSerializer(serializers.ModelSerializer):
    cart_products = ProductSerializer(many=True, read_only=True)   
    class Meta:
        model = Product
        fields ='__all__'         
        required = True   

class CartItemSerializer(serializers.ModelSerializer):    
    # cart_deatils = serializers.SerializerMethodField('get_cart_deatils')
    cart_products = serializers.SerializerMethodField('get_cart_products')
    price = serializers.SerializerMethodField('get_price')

    def get_price(sel, cartitem):
        return cartitem.quantity * cartitem.product.price  
      
    def get_cart_deatils(self, obj): 
        cart_deatils = {}
        cart_obj = Cart.objects.filter(id=obj.id)
        if len(cart_obj)>0:
            cart_deatils = ProductSerializer(cart_obj[0]).data
        else:
            cart_deatils = cart_deatils            
        return cart_deatils  
    
    def get_cart_products(self, obj): 
        product_detail = {}
        product_obj = Product.objects.filter(id=obj.id)
        if len(product_obj)>0:
            product_detail = ProductSerializer(product_obj[0]).data
        else:
            product_detail = product_detail
        return product_detail   
            
       
    class Meta:
        model = CartItem
        fields =['id', 'quantity', 'price', 'cart_products']
        # extra_fields = ['cart_products', 'cart_deatils']  
        required = True  


class AddCartItemSerializer(serializers.ModelSerializer):
    def save(self, **obj):
        cart_item = CartItem.objects.filter(product=obj.product).exists()
        if cart_item:
            CartItem.objects.filter(product=obj.product).update(cart=obj.cart, product=obj.product, quantity=obj.quantity)
        else:                    
            return CartItem.objects.create(**obj)  

    class Meta:
        model = CartItem
        fields =['id', 'product', 'quantity']           

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4())     
    cart_deatils = CartItemSerializer(many=True, read_only=True)  
    user=serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())  
    class Meta:
        model = Cart
        fields ='__all__'
        required = True

class UserCartSerializer(serializers.ModelSerializer):
    user_cart = CartSerializer()  
    class Meta:
        model = User
        fields =['id', 'name', 'email', 'user_code', 'user_cart']  
        required = True 
   
class UserCartItems(serializers.ModelSerializer):
    cart_deatils = CartItemSerializer(many=True, read_only=True) 
    cart_products = ProductItemSerializer(source='cart_products.id')
    class Meta:
        # unique_together = ("cart_deatils", "cart_deatils")
        model = Cart
        fields ='__all__'
        depth = 1
        required = True
      
      
