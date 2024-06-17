from django.contrib import admin
from django.utils.html import format_html
from .models import *
from members.models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','category']
    list_filter = ['category']

    # def image_show(self,img):
    #     return format_html('<img src="{}" style="border: #232323 1px solid; border-radius: 5%;"  width="100" height="100" />', img.image.url) if img.image else ''

class MeasureSizeAdmin(admin.ModelAdmin):
    list_display = ('order', 'h', 'w', 'd', 'note')
    search_fields = ('order__first_name', 'order__last_name')  # ค้นหาโดยใช้ชื่อลูกค้า
    list_filter = ('order__status',) 
    

    def orders(self,order):
        return order.order.user if order.order else ''

    def order_id(self,order):
        return order.order.id if order.order else ''

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id','image']
    ordering = ['id']

class WorkingDayAdmin(admin.ModelAdmin):
    list_display = ['date_work']    

admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Material)
admin.site.register(MeasureSize,MeasureSizeAdmin)
admin.site.register(ProductImage,ProductImageAdmin)
admin.site.register(WorkingDay,WorkingDayAdmin)