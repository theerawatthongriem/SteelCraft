from django import forms

from manager.models import Product, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        labels = {
            
            'name':'ชื่อสินค้า',
            'description':'คำอธิบายสินค้า',
            'category':'หมวดหมู่',
        }

        exclude = ['user','price','product_deposit']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

        widgets = {
            'image': forms.FileInput(attrs={'class': 'my-2'}),
        }