from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/',manager_dashboard, name="manager_dashboard"),
    path('customer_orders/',customer_orders, name="customer_orders"),
    path('add_product/',add_product, name="add_product"),
    path('edit_product/<int:id>/',edit_product, name="edit_product"),
    path('delete_product/<int:id>/',delete_product, name="delete_product"),
    path('order_detail/<int:id>/',order_detail, name="order_detail"),
    path('material_list/',material_list, name="material_list"),
    path('add_material/',add_material, name="add_material"),
    path('size_save/',size_save, name="size_save"),
    path('size_save_detail/<int:id>/',size_save_detail, name="size_save_detail"),
    path('add_size/<int:id>/',add_size, name="add_size"),
    path('get_size/<int:id>/', get_size, name='get_size'),
    path('delete_size/<int:id>/<int:dlt>/', delete_size, name='delete_size'),
    path('edit_size/<int:id>/<int:dlt>/', edit_size, name='edit_size'),

]