from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        labels = {
            'name':'ชื่อสินค้า',
            'description':'คำอธิบายสินค้า',
            'price':'ราคา',
            'image':'รูปภาพ',
            'category':'หมวดหมู่',
        }