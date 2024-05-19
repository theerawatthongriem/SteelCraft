from django.shortcuts import render,redirect
from .models import *
from manager.models import Product
from django.contrib import messages
from base_app.models import UserMessage

from django.contrib.auth.decorators import login_required ,user_passes_test

from base_app.context_processors import favorite_count
from .permissions import *
from base_app.views import send_line_message

from promptpay import qrcode
import base64
from io import BytesIO

from manager.forms import DepositForm,PaymentForm


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
def checkout(request,id):
    product = Product.objects.get(pk=id)
    return render(request,'members/checkout.html',{'product':product, 'favorite_count':favorite_count(request)})

@login_required(login_url='login')
def create_order(request,id):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    quantity = request.POST.get('quantity')
    address = request.POST.get('address')
    phone_number = request.POST.get('phone_number')
    note = request.POST.get('note')
    delivery_location = request.POST.get('delivery_location')
    appt_date = request.POST.get('appt_date')
    product = Product.objects.get(pk=id)
    product_category = product.category
    total_price = int(product.price) * int(quantity)
    deposit = product.product_deposit
    total_pay = total_price - deposit

    print(
    quantity,
    address,
    phone_number,
    note,
    delivery_location,
    product,
    product_category,
    total_price,
    first_name,
    last_name,
    )

    order = Order.objects.create(
        user=request.user,
        product=product,
        price=product.price,
        quantity=quantity,
        total_price=total_price,
        address=address,
        phone_number=phone_number,
        note=note,
        product_category=product_category,
        delivery_location=delivery_location,
        first_name=first_name,
        last_name=last_name,
        appt_date=appt_date,
        deposit=deposit,
        total_pay=total_pay,
    )

    order.save()
    user_order = Order.objects.filter(user=request.user).order_by('-id').first()
    data = UserMessage.objects.filter(user=request.user).first()
    if data:
        message = (f'คำสั่งซื้อ : {user_order.id}  {user_order.product.name} \n จำนวน {user_order.quantity} รายการ ราคารวม {user_order.total_price} บาท \n - การจัดส่ง \n คุณ {user_order.first_name} {user_order.last_name} \n{user_order.address} \n {user_order.phone_number}')
        # if data.line_id:
        #     send_line_message(data.line_id, message)

    return redirect(f'orders')

@login_required(login_url='login')
def order_list(request):
    order = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request,'members/order_list.html',{'orders':order, 'favorite_count':favorite_count(request)})

# def order_detail(request,id):
#     order = Order.objects.get(pk=id)
#     return render(request, 'members/order_detail.html',{'order':order})


@login_required(login_url='login')
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

    





