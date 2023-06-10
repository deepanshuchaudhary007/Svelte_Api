from django.urls import path
from products import views

urlpatterns = [
    ### Endpoints For Category  Start #######
    path('all_category/', views.all_category, name='all_category'), 
    path('category_details/<str:slug>', views.category_details, name='category_details'),
    path('create_category/', views.create_category, name='create_category'),   
    path('category_update/<str:slug>', views.category_update, name='category_update'),    
    path('category_delete/<str:slug>', views.category_delete, name='category_delete'), 
    ### Endpoints For Category Ends #######

    ### Endpoints For Products Start #######
    path('create_product/', views.create_product, name='create_products' ),
    path('all_product/', views.all_product, name='all_product'), 
    path('product_details/<str:slug>', views.product_details, name='product_details'),      
    path('product_update/<str:slug>', views.product_update, name='product_update'),    
    path('product_delete/<str:slug>', views.product_delete, name='product_delete'), 
    path('product_on_category/<str:slug>', views.product_on_category, name='product_on_category'),
    ### Endpoints For Products Ends #######

    ### Endpoints For Products Image Start #######
    path('add_product_image/', views.create_product, name='create_products' ),         
    path('update_product_image/<str:id>', views.product_update, name='product_update'),    
    path('delete_product_image/<str:id>', views.product_delete, name='product_delete'),
    ### Endpoints For Products Image Ends #######
]