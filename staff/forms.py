from django import forms
from members.models import *

class OrderForm(forms.ModelForm):
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
    
