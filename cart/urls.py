from django.urls import path
from cart import views

urlpatterns = [
    path('add_to_cart/', views.add_to_cart, name='add_to_cart' ), 
    # path('cart_details/', views.cart_details, name="cart_details"),
    path('update_cart/<int:id>', views.update_cart, name='update_cart'), 
    path('cart_items/<int:id>', views.cart_items, name='cart_items'),   
    path('user_cart/<str:user_code>', views.user_cart, name='user_cart'),  
    path('user_cart_items/<str:id>', views.user_cart_items, name='user_cart_items'),
    path('delete_cart_item/<str:id>', views.delete_cart_item, name='delete_cart_item'), 
]