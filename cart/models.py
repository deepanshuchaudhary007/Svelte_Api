import uuid
from django.db import models
from products.models import Product
from users.models import User
# Create your models here.


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), unique=True, editable=False)
    user = models.OneToOneField(User, related_name="user_cart", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)   

    def __str__(self) -> str:
        return str(self.user.name)
    
    
class CartItem(models.Model):    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_deatils") 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name="cart_products")
    quantity = models.IntegerField(default=0)
    price = models.FloatField()

    def __str__(self) -> str:
        return str(self.product.name)
    

# class CartItem(models.Model) :
#     user = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
#     ordered = models.BooleanField(default=False)
#     item = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True)
#     quantity = models.IntegerField(default=1)


#     def __str__(self):
#         return f"{self.quantity} of {self.item.name}"

# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
#     items = models.ManyToManyField(CartItem,blank=True, null=True)
#     start_date = models.DateTimeField(auto_now_add=True)
#     ordered_date = models.DateTimeField()
#     ordered = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.email    