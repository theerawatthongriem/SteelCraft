from django.contrib import admin
from .models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'product', 'product_category', 'price', 'quantity', 'total_price', 'address', 'delivery_location', 'phone_number', 'note', 'order_date', 'status']

class CancellationReasonAdmin(admin.ModelAdmin):
    list_display = ['cancellation_reason']

admin.site.register(Order, OrderAdmin)
admin.site.register(CancellationReason, CancellationReasonAdmin)
admin.site.register(CancelOrder)
# admin.site.register(UserMessage)
