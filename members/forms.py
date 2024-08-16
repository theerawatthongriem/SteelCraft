from django import forms
from .models import Order

from manager.models import Product, ProductImage


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'quantity', 'address', 'phone_number', 'note', 'delivery_location', 'appt_date']
        
    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.fields['appt_date'].widget = forms.DateInput(attrs={'type': 'date'})


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        labels = {
            
            'name':'ชื่อสินค้า',
            'description':'คำอธิบายสินค้า',
            'category':'หมวดหมู่',
        }

        exclude = ['user','price','product_deposit','production_time',]

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

        widgets = {
            'image': forms.FileInput(attrs={'class': 'my-2'}),
        }