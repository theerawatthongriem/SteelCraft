from django import forms
from .models import * 
from members.models import Order,MeasureSize
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

class DepositForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['deposit_proof']
        labels = {'deposit_proof':'ไฟล์'}

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_proof']
        labels = {'payment_proof':'ไฟล์'}

class MeasureSizeForm(forms.ModelForm):
    class Meta:
        model = MeasureSize
        fields = '__all__'
        exclude = ['order']

        labels = {
            'h':'สูง' ,
            'w':'กว้าง' ,
            'd':'หนา' ,
            'image1':'รูปภาพ 1 (ถ้ามี)',
            'image2':'รูปภาพ 2 (ถ้ามี)',
            'image3':'รูปภาพ 3 (ถ้ามี)',
            'image4':'รูปภาพ 4 (ถ้ามี)',
            'image5':'รูปภาพ 5 (ถ้ามี)',
            'image6':'รูปภาพ 6 (ถ้ามี)',
            'note':'หมายเหตุ',
        }