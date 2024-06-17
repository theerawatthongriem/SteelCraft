from django.urls import path
from .views import *

urlpatterns = [
    path('staff_dashboard/',staff_dashboard,name='staff_dashboard'),
    path('staff_order_list/',staff_order_list,name='staff_order_list'),
    path('staff_orders_category/<str:status>/',staff_orders_category,name='staff_orders_category'),
    path('staff_size_save/',staff_size_save,name='staff_size_save'),
    path('staff_edit_order/<int:id>/',staff_edit_order,name='staff_edit_order'),
]