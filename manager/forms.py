from django import forms
from .models import * 
from members.models import Order,MeasureSize,MeasureSizeMaterial
from django.forms import formset_factory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.utils.dateformat import format

from datetime import datetime

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
            'production_time':'ระยะเวลาผลิต(วัน)',
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
            
            'image': forms.FileInput(attrs={'class': 'my-2','required': True}),
        }


class EditProductImageForm(forms.ModelForm):
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
        fields = ['price', 'total_price', 'deposit', 'total_pay', 'appt_date', 'ship_date','staff']
        labels = {
            'price': 'ราคา',
            'total_price': 'ราคารวม',
            'deposit': 'ค่ามัดจำ ( % )',
            'total_pay': 'ยอดชำระคงเหลือ',
            'appt_date': 'วันนัดวัดขนาด',
            'ship_date': 'วันจัดส่ง/ติดตั้ง',
            'staff': 'พนักงาน ที่รับผิดชอบ',
        }
        widgets = {
            'price': forms.NumberInput(attrs={'class':'numberinput bg-white border-gray-300 py-2 border block text-gray-700 px-4 leading-normal w-full appearance-none rounded-lg focus:outline-none'}),
            'total_price': forms.NumberInput(attrs={'class':'numberinput bg-white border-gray-300 py-2 border block text-gray-700 px-4 leading-normal w-full appearance-none rounded-lg focus:outline-none'}),
            'deposit': forms.NumberInput(attrs={'class':'numberinput bg-white border-gray-300 py-2 border block text-gray-700 px-4 leading-normal w-full appearance-none rounded-lg focus:outline-none'}),
            'total_pay': forms.NumberInput(attrs={'class':'numberinput bg-white border-gray-300 py-2 border block text-gray-700 px-4 leading-normal w-full appearance-none rounded-lg focus:outline-none'}),

            'ship_date': forms.DateTimeInput(format='%Y-%m-%d',attrs={'class': 'my-2 block w-full border rounded-md py-2 px-3 form-control', 'type': 'date',}),
            'appt_date': forms.DateTimeInput(format='%Y-%m-%d',attrs={'class': 'my-2 block w-full border rounded-md py-2 px-3', 'type': 'date'}),
            'staff': forms.Select(attrs={'class': 'my-2 block w-full border rounded-md py-2 px-3'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['staff'].queryset = User.objects.filter(is_staff=True,is_active=True,is_superuser=False)
        self.fields['staff'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}   กำลังดำเนินการอยู่  {self.get_staff_label(obj)}"

    def get_staff_label(self, obj):
        order_count = Order.objects.filter(staff=obj).exclude(status__in=['เสร็จสิ้น', 'ยกเลิก']).count()
        return order_count

class StaffOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['price', 'total_price', 'deposit', 'total_pay', 'appt_date', 'ship_date',]
        labels = {
            'price': 'ราคา',
            'total_price': 'ราคารวม',
            'deposit': 'ค่ามัดจำ ( % )',
            'total_pay': 'ยอดชำระคงเหลือ',
            'appt_date': 'วันนัดวัดขนาด',
            'ship_date': 'วันจัดส่ง/ติดตั้ง',
        }
        widgets = {
            'ship_date': forms.DateTimeInput(format='%Y-%m-%d',attrs={'class': 'my-2 block w-full border rounded-md py-2 px-3 form-control datepicker', 'type': 'date',}),
            'appt_date': forms.DateTimeInput(format='%Y-%m-%d',attrs={'class': 'my-2 block w-full border rounded-md py-2 px-3', 'type': 'date'}),
        }
    


class OrderInstallProofsForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['image1','image2','image3','image4']
        labels = {
            'image1': 'รูปภาพ 1',
            'image2': 'รูปภาพ 2',
            'image3': 'รูปภาพ 3',
            'image4': 'รูปภาพ 4',
        }


class AddStaffForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2',]

class EditStaffForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email',]

class DateSelectionForm(forms.Form):
    current_year = datetime.now().year
    YEARS = [(year, year) for year in range(2020, current_year + 1)]
    MONTHS = [
        (1, 'มกราคม'), (2, 'กุมภาพันธ์'), (3, 'มีนาคม'), (4, 'เมษายน'),
        (5, 'พฤษภาคม'), (6, 'มิถุนายน'), (7, 'กรกฎาคม'), (8, 'สิงหาคม'),
        (9, 'กันยายน'), (10, 'ตุลาคม'), (11, 'พฤศจิกายน'), (12, 'ธันวาคม')
    ]

    month = forms.ChoiceField(choices=MONTHS, label='เดือน', initial=datetime.now().month)
    year = forms.ChoiceField(choices=YEARS, label='ปี', initial=current_year)

    
class WorkingDayForm(forms.ModelForm):
    class Meta:
        model = WorkingDay
        fields = ['date_work']
        widgets = {
            'date_work': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'date_work': 'วันที่',
        }
