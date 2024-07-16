from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/',manager_dashboard, name="manager_dashboard"),
    path('overwiew/',overwiew, name="overwiew"),

    path('customer_orders/',customer_orders, name="customer_orders"),
    path('customer_orders_category/<str:status>/',customer_orders_category, name="customer_orders_category"),

    
    path('add_product/',add_product, name="add_product"),
    path('edit_product/<int:id>/',edit_product, name="edit_product"),
    path('update_product/<int:product_id>/',update_product, name="update_product"),
    path('product/delete_image/<int:image_id>/', delete_image, name='delete_image'),
    path('delete_product/<int:id>/',delete_product, name="delete_product"),
    path('order_detail/<int:id>/',order_detail, name="order_detail"),
    path('material_list/',material_list, name="material_list"),
    path('add_material/',add_material, name="add_material"),
    path('size_save/',size_save, name="size_save"),
    path('size_save_detail/<int:id>/',size_save_detail, name="size_save_detail"),
    path('add_size/<int:id>/',add_size, name="add_size"),

    # path('get_size/<int:id>/', get_size, name='get_size'),

    path('delete_size/<int:id>/<int:dlt>/', delete_size, name='delete_size'),
    path('edit_size/<int:id>/<int:dlt>/', edit_size, name='edit_size'),
    path('update_status/<int:id>/<str:status>/', update_status, name='update_status'),
    path('upload_deposit/<int:id>/', upload_deposit, name='upload_deposit'),
    path('upload_payment/<int:id>/', upload_payment, name='upload_payment'),
    path('confirm_deposit/<int:id>/', confirm_deposit, name='confirm_deposit'),
    path('confirm_payment/<int:id>/', confirm_payment, name='confirm_payment'),
    path('cancel_order/<int:id>/', cancel_order, name='cancel_order'),
    path('size_save_detail/<int:id>/<int:dlt>/edit_size/<int:q>/', edit_size, name='edit_size'),
    path('measure_size_detail/<int:measure_size_id>/<int:q>/', measure_size_detail, name='measure_size_detail'),
    path('update_material/<int:id>/<str:action>/', update_material, name='update_material'),

    path('add_category/',add_category, name='add_category'),
    path('edit_category/<int:id>/<str:action>/',edit_category, name='edit_category'),
    path('edit_order/<int:id>/',edit_order, name='edit_order'),

    path('material_order/',material_order, name='material_order'),
    path('staff_manager/',staff_manager, name='staff_manager'),
    path('edit_staff_manager/<int:id>/',edit_staff_manager, name='edit_staff_manager'),
    path('delete_staff/<int:id>/',delete_staff, name='delete_staff'),
    path('order_install_proofs/<int:id>/',order_install_proofs, name='order_install_proofs'),

    path('add_working_day/',add_working_day, name='add_working_day'),
    path('delete-working-day/<str:date_work>/', delete_working_day, name='delete_working_day'),

]