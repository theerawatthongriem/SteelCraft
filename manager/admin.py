from django.contrib import admin
from django.utils.html import format_html
from .models import *
from members.models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','category']

    # def image_show(self,img):
    #     return format_html('<img src="{}" style="border: #232323 1px solid; border-radius: 5%;"  width="100" height="100" />', img.image.url) if img.image else ''

class MeasureSizeAdmin(admin.ModelAdmin):
    list_display = ['orders','order_id','h','w','d']

    def orders(self,order):
        return order.order.user if order.order else ''

    def order_id(self,order):
        return order.order.id if order.order else ''


admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Material)
admin.site.register(MeasureSize,MeasureSizeAdmin)
admin.site.register(ProductImage)