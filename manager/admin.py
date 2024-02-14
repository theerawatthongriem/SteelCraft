from django.contrib import admin
from django.utils.html import format_html
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','image_show','category']

    def image_show(self,img):
        return format_html('<img src="{}" style="border: #232323 1px solid; border-radius: 5%;"  width="100" height="100" />', img.image.url) if img.image else ''


admin.site.register(Product,ProductAdmin)
admin.site.register(Category)