from django import forms
from .models import * 
from django.forms import formset_factory


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        labels = {
            'name':'ชื่อสินค้า',
            'description':'คำอธิบายสินค้า',
            'price':'ราคา',
            'category':'หมวดหมู่',
        }

        exclude = ['user']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

        widgets = {
            'image': forms.FileInput(attrs={'class': 'my-2'}),
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'

        labels = {
            'name':'ชื่อวัสดุ',
            'quantity':'จำนวน',
            'image':'รูปภาพ',
        }