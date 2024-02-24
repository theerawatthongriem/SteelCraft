from django.shortcuts import render,redirect
from .models import *
from manager.models import Product
from django.contrib import messages

from django.contrib.auth.decorators import login_required ,user_passes_test

from base_app.context_processors import favorite_count
from .permissions import *

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
    return redirect(f'/product_detail/{id}/')

@login_required(login_url='login')
def order_list(request):
    order = Order.objects.filter(user=request.user)
    return render(request,'members/order_list.html',{'orders':order, 'favorite_count':favorite_count(request)})



    





