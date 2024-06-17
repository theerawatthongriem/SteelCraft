from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from manager.models import Product,WorkingDay
from django.contrib import messages
from base_app.models import UserMessage

from django.contrib.auth.decorators import login_required ,user_passes_test

from base_app.context_processors import favorite_count
from .permissions import *
from base_app.views import send_line_message

from promptpay import qrcode
import base64
from io import BytesIO
from django.forms import formset_factory
from .forms import *


from manager.forms import DepositForm,PaymentForm
from django.core.paginator import Paginator

from django.utils import timezone
from datetime import timedelta,datetime

import json
from django.core.serializers.json import DjangoJSONEncoder




@login_required(login_url='login')
def add_favorite(request,id):
    product = Product.objects.get(pk=id)
    favorite = Favorite.objects.create(user=request.user,product=product)
    favorite.save()

    messages.success(request, 'สินค้าถูกเพิ่มในรายการโปรดแล้ว')

    return redirect(f'/product_detail/{id}/')


@login_required(login_url='login')
def favorite(request):
    favorite = Favorite.objects.filter(user=request.user)
    return render(request,'members/favorite.html',{'fav':favorite, 'favorite_count':favorite_count(request)})


@login_required(login_url='login')
def delete_favorite(request,id):
    favorite = Favorite.objects.get(pk=id,user=request.user)
    favorite.delete()
    return redirect('fav')

@login_required(login_url='login')
def checkout(request, id):


    working_days = list(WorkingDay.objects.all().values('date_work'))

    for day in working_days:
        day['date_work'] = day['date_work'].strftime('%Y-%m-%d')

   

    product = get_object_or_404(Product, pk=id)
    error_message = None

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_staff or request.user.is_superuser:
                order.user = None
                order.staff = request.user
            else:
                order.user = request.user

            order.user = request.user
            order.product = product
            order.product_category = product.category
            order.price = product.price
            order.total_price = int(product.price) * int(form.cleaned_data['quantity'])
            order.deposit = product.product_deposit
            order.total_pay = order.total_price - order.deposit


            ship_date = product.production_time * int(form.cleaned_data['quantity'])


            tomorrow = timezone.now().date() + timedelta(days=1)
            appt_date_parsed = form.cleaned_data['appt_date']
            if appt_date_parsed and appt_date_parsed < tomorrow:
                error_message = 'วันนัดวัดขนาดต้องเลือกวันถัดไป และไม่ตรงกับวันหยุดทำการ'
            else:
                order.appt_date = timezone.make_aware(timezone.datetime.combine(appt_date_parsed, timezone.datetime.min.time()))
                order.ship_date = timezone.make_aware(timezone.datetime.combine(appt_date_parsed, timezone.datetime.min.time())) + timedelta(days=ship_date)  # เพิ่ม 5 วันให้กับ appt_date
                order.save()
                if request.user.is_superuser:
                    return redirect('customer_orders')
                elif request.user.is_staff:
                    return redirect('staff_order_list')
                else:
                    return redirect('orders')
        else:
            error_message = 'ข้อมูลไม่ถูกต้อง กรุณาตรวจสอบอีกครั้ง'
    else:
        form = CheckoutForm()

    return render(request, 'members/checkout.html', {
        'product': product,
        'form': form,
        'error_message': error_message,
        'working_days': json.dumps(working_days),
    })



@login_required(login_url='login')
def order_list(request):

    order_status = Order.objects.first()


    order = Order.objects.filter(user=request.user).order_by('-order_date')

    paginator = Paginator(order, 8)
    page = request.GET.get('page', 1)  
    order = paginator.get_page(page)
    
    return render(request,'members/order_list.html',{'orders':order, 'favorite_count':favorite_count(request),'order_status':order_status})

@login_required(login_url='login')
def customer_orders_category(request,status):

    order_status = Order.objects.first()

    order = Order.objects.filter(status=status,user=request.user).order_by('-order_date')

    paginator = Paginator(order, 8)
    page = request.GET.get('page', 1)  
    order = paginator.get_page(page)
    
    return render(request,'members/order_list_category.html',{
        'orders':order, 
        'favorite_count':favorite_count(request),
        'order_status':order_status,
        'status':status,
    })

# @login_required(login_url='login')
def order_detail(request,id):

    order = Order.objects.get(pk=id)

    id_or_phone_number = "0956452530"
    amount = order.total_price

    

    deposit_price = order.total_price * (order.deposit)/100
    last_price = order.total_price - deposit_price

    payload_with_amount1 = qrcode.generate_payload(id_or_phone_number, deposit_price)
    qr_img1 = qrcode.to_image(payload_with_amount1)

    qr_img_bytesio1 = BytesIO()
    qr_img1.save(qr_img_bytesio1, format='PNG')
    qr_img_base641 = base64.b64encode(qr_img_bytesio1.getvalue()).decode('utf-8')


    payload_with_amount = qrcode.generate_payload(id_or_phone_number, last_price)
    qr_img = qrcode.to_image(payload_with_amount)

    qr_img_bytesio = BytesIO()
    qr_img.save(qr_img_bytesio, format='PNG')
    qr_img_base64 = base64.b64encode(qr_img_bytesio.getvalue()).decode('utf-8')

    form = DepositForm(instance=order)
    form2 = PaymentForm(instance=order)

    print(order.deposit_payment)


    return render(request, 'members/order_detail.html',{
        'order':order,
        'qr_img_base64':qr_img_base64,
        'qr_img_base641':qr_img_base641,
        'deposit_price':int(deposit_price),
        'last_price':int(last_price),
        'forms':form,
        'forms2':form2,
        })


def add_product_user(request):

    ImageFormSet = formset_factory(ProductImageForm, extra=3)  # extra คือจำนวนฟอร์มที่สร้างขึ้นมาเริ่มต้น
    
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES)
        if product_form.is_valid() and formset.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()
            for form in formset:
                image = form.cleaned_data.get('image')
                ProductImage.objects.create(product=product, image=image)
            return redirect('product_members')
    else:
        product_form = ProductForm()
        formset = ImageFormSet()
    
    return render(request, 'members/add_product_user.html', {'product_form': product_form, 'formset': formset,})





