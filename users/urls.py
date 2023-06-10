from django.urls import path
from users import views

urlpatterns = [
    path('country/', views.country, name='country'),
    path('state/<str:country_id>', views.state, name='state'),
    path('city/<str:state_id>', views.city, name='city'),
    path('registeration/', views.registeration, name='registeration'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),    
    path('change_password/', views.password_change, name='change_password'),
    path('user_update/<str:user_code>', views.user_update, name='user_update'),
    path('forgot_password_link/', views.forgot_password_link, name='forgot_password_link'),
    path('forgot_password/<uid>/<token>', views.forgot_password, name='forgot_password'),
    path('add_profile_pic/', views.add_profile_pic, name='add_profile_pic'),
    path('update_profile_pic/', views.update_profile_pic, name='update_profile_pic'),
    path('delete_profile_pic/', views.delete_profile_pic, name='delete_profile_pic'),
    path('profile/<str:user_code>', views.profile, name='profile'),
]

