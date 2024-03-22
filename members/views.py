from django.shortcuts import render,redirect
from .models import *
from manager.models import Product
from django.contrib import messages
from base_app.models import UserMessage

from django.contrib.auth.decorators import login_required ,user_passes_test

from base_app.context_processors import favorite_count
from .permissions import *
from base_app.views import send_line_message

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
    product = Product.objects.get(pk=id)
    product_category = product.category
    total_price = int(product.price) * int(quantity)

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
    )

    order.save()
    user_order = Order.objects.filter(user=request.user).order_by('-id').first()
    data = UserMessage.objects.filter(user=request.user).first()
    if data:
        message = (f'คำสั่งซื้อ : {user_order.id}  {user_order.product.name} \n จำนวน {user_order.quantity} รายการ ราคารวม {user_order.total_price} บาท \n - การจัดส่ง \n คุณ {user_order.first_name} {user_order.last_name} \n{user_order.address} \n {user_order.phone_number}')
        # if data.line_id:
        #     send_line_message(data.line_id, message)

    return redirect(f'/product_detail/{id}/')

@login_required(login_url='login')
def order_list(request):
    order = Order.objects.filter(user=request.user)
    return render(request,'members/order_list.html',{'orders':order, 'favorite_count':favorite_count(request)})

@login_required(login_url='login')
def order_detail(request,id):
    order = Order.objects.get(pk=id)
    return render(request, 'members/order_detail.html',{'order':order})



    





