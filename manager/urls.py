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
]