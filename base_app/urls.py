from django.urls import path
from .views import *

urlpatterns = [

    path('',home,name='home'),
    path('line/',line,name='line'),
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
    path('product_members/', product_members, name='product_members'),
    
    path('connect_line_user/', connect_line_user, name='connect_line_user'),
    path('webhook/', webhook, name='webhook'),

    # path('search/results/', search_results_view, name='search_results_view'),
    # path('search/', search_view, name='search'),


]