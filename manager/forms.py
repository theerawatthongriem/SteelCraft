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

        exclude = ['user']

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'

        labels = {
            'name':'ชื่อวัสดุ',
            'quantity':'จำนวน',
            'image':'รูปภาพ',
        }