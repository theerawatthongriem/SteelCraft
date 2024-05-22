from django import forms
from .models import * 
from members.models import Order,MeasureSize,MeasureSizeMaterial
from django.forms import formset_factory


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.utils.dateformat import format


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        labels = {
            
            'name':'ชื่อสินค้า',
            'product_deposit':'ค่ามัดจำสินค้า ( % )',
            'description':'คำอธิบายสินค้า',
            'price':'ราคา',
            'category':'หมวดหมู่',
        }

        exclude = ['user']

class CategoryForm(forms.ModelForm):
    class Meta:
        model =  Category
        fields = '__all__'

        labels = {
            
            'name':'ชื่อหมวดหมู่',
        }


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
            'h':'สูง (ซม.)' ,
            'w':'กว้าง (ซม.)' ,
            'd':'หนา (ซม.)' ,
            'image1':'รูปภาพ 1 (ถ้ามี)',
            'image2':'รูปภาพ 2 (ถ้ามี)',
            'image3':'รูปภาพ 3 (ถ้ามี)',
            'image4':'รูปภาพ 4 (ถ้ามี)',
            'image5':'รูปภาพ 5 (ถ้ามี)',
            'image6':'รูปภาพ 6 (ถ้ามี)',
            'note':'หมายเหตุ',
        }

class MeasureSizeMaterialForm(forms.ModelForm):
    class Meta:
        model = MeasureSizeMaterial
        fields = ['material', 'quantity']

        labels = {
            'material':'วัสดุ' ,
            'quantity':'จำนวน',
            }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['price', 'total_price', 'deposit', 'total_pay', 'appt_date', 'ship_date']
        labels = {
            'price': 'ราคา',
            'total_price': 'ราคารวม',
            'deposit': 'ค่ามัดจำ ( % )',
            'total_pay': 'ยอดชำระคงเหลือ',
            'appt_date': 'วันนัดวัดขนาด',
            'ship_date': 'วันจัดส่ง/ติดตั้ง',
        }
        widgets = {
            'ship_date': forms.DateTimeInput(attrs={'class': 'my-2 block w-full border rounded-md py-2 px-3', 'type': 'datetime-local'}),
            'appt_date': forms.DateTimeInput(attrs={'class': 'my-2 block w-full border rounded-md py-2 px-3', 'type': 'datetime-local'}),
        }



        # exclude = ['user','product','status','product_category']