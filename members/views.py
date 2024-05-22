from django.shortcuts import render,redirect,get_object_or_404
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
from django.forms import formset_factory
from .forms import *


from manager.forms import DepositForm,PaymentForm
from django.core.paginator import Paginator

from django.utils import timezone
from datetime import timedelta



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
    product = get_object_or_404(Product, pk=id)
    error_message = None

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        quantity = request.POST.get('quantity')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        note = request.POST.get('note')
        delivery_location = request.POST.get('delivery_location')
        appt_date = request.POST.get('appt_date')
        product_category = product.category
        total_price = int(product.price) * int(quantity)
        deposit = product.product_deposit
        total_pay = total_price - deposit

        tomorrow = timezone.now() + timedelta(days=1)
        try:
            appt_date_parsed = timezone.datetime.strptime(appt_date, '%Y-%m-%d')
            appt_date_parsed = timezone.make_aware(appt_date_parsed, timezone.get_default_timezone())
        except ValueError:
            error_message = 'รูปแบบวันที่ไม่ถูกต้อง'
            appt_date_parsed = None

        if appt_date_parsed and appt_date_parsed < tomorrow:
            error_message = 'วันนัดวัดขนาดต้องไม่เร็วกว่าวันพรุ่งนี้'
        else:
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
                appt_date=appt_date_parsed,
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

            return redirect('orders')

    return render(request, 'members/checkout.html', {
        'product': product,
        'error_message': error_message,
        'form_data': request.POST if request.method == 'POST' else None,
    })



# @login_required(login_url='login')
# def create_order(request,id):
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         quantity = request.POST.get('quantity')
#         address = request.POST.get('address')
#         phone_number = request.POST.get('phone_number')
#         note = request.POST.get('note')
#         delivery_location = request.POST.get('delivery_location')
#         appt_date = request.POST.get('appt_date')
#         product = Product.objects.get(pk=id)
#         product_category = product.category
#         total_price = int(product.price) * int(quantity)
#         deposit = product.product_deposit
#         total_pay = total_price - deposit

#         error_message = None
#         tomorrow = timezone.now() + timedelta(days=1)
#         if appt_date and appt_date < tomorrow:
#             error_message = 'วันนัดวัดขนาดต้องไม่เร็วกว่าวันพรุ่งนี้'
#             return redirect(f'/members/checkout/product/{id}/')
#         else:
#             order = Order.objects.create(
#             user=request.user,
#             product=product,
#             price=product.price,
#             quantity=quantity,
#             total_price=total_price,
#             address=address,
#             phone_number=phone_number,
#             note=note,
#             product_category=product_category,
#             delivery_location=delivery_location,
#             first_name=first_name,
#             last_name=last_name,
#             appt_date=appt_date,
#             deposit=deposit,
#             total_pay=total_pay,
#         )

#             order.save()
#             user_order = Order.objects.filter(user=request.user).order_by('-id').first()
#             data = UserMessage.objects.filter(user=request.user).first()
#             if data:
#                 message = (f'คำสั่งซื้อ : {user_order.id}  {user_order.product.name} \n จำนวน {user_order.quantity} รายการ ราคารวม {user_order.total_price} บาท \n - การจัดส่ง \n คุณ {user_order.first_name} {user_order.last_name} \n{user_order.address} \n {user_order.phone_number}')
#                 # if data.line_id:
#                 #     send_line_message(data.line_id, message)

#             return redirect(f'orders')



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





