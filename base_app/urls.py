from django.urls import path
from .views import *

urlpatterns = [

    path('',home,name='home'),
    path('register/',register,name='register'),
    path('login/',sign_in,name='login'),
    path('logout/',sign_out,name='logout'),
    path('profile/',profile,name='profile'),
    path('editprofile/',editprofile,name='editprofile'),
    path('change_password/',change_password,name='change_password'),
    path('delete_user/',delete_user,name='delete_user'),
    path('dashboard/',dashboard,name='dashboard'),
    path('product_list/',product_list,name='product_list'),
    path('product_detail/<int:id>/',product_detail,name='product_detail'),

    path('found_page/',found_page,name='found_page'),

    path('line-user/<str:user_id>/', bind_line_user, name='line_user'),

]