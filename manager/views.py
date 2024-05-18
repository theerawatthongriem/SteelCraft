from django.shortcuts import render,redirect,get_object_or_404
from members.models import Order,MeasureSize
from .forms import *
from base_app.context_processors import favorite_count
from django.contrib.auth.decorators import user_passes_test,login_required

from django.db.models import Count, OuterRef, Subquery, IntegerField
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.forms import formset_factory


import plotly.graph_objs as go

from .permissions import *

from promptpay import qrcode
from members.models import *

from django.core.paginator import Paginator

# import qrcode
import base64
from io import BytesIO
# from django.http import HttpResponse


# def generate_promptpay_qr(request):
#     # สร้างข้อมูล PromptPay
#     promptpay_id = "0956452530"  # เบอร์โทรศัพท์หรือเลขบัญชี PromptPay
#     amount = "100"  # จำนวนเงิน

#     # สร้าง URL สำหรับ PromptPay
#     promptpay_url = f"promptpay://{promptpay_id}?amount={amount}"

#     # สร้าง QR code
#     qr = qrcode.make(promptpay_url)

#     # แปลง QR code เป็น BytesIO object
#     qr_bytes = BytesIO()
#     qr.save(qr_bytes, format='PNG')
#     qr_bytes.seek(0)

#     # สร้าง HttpResponse สำหรับแสดง QR code บนเว็บ
#     response = HttpResponse(qr_bytes, content_type='image/png')
#     return response

@login_required(login_url='login')
@user_passes_test(manager_user,login_url='found_page')
def manager_dashboard(request):
    
    product_counts = Order.objects.filter(
    product__category=OuterRef('pk')
    ).values('product__category').annotate(
        num_products=Count('id')
    ).values('num_products')

    # สร้าง queryset สำหรับการแสดง category ทั้งหมด
    categories_with_counts = Category.objects.annotate(
        num_products=Coalesce(Subquery(product_counts), 0, output_field=IntegerField())
    )

    # สร้าง list ของชื่อ category และจำนวนสินค้าที่สั่งซื้อ
    category_names = [category.name for category in categories_with_counts]
    product_counts = [category.num_products for category in categories_with_counts]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=category_names, y=product_counts))

    
    fig.update_layout(
    title='จำนวนสินค้าในแต่ละหมวดหมู่',
    xaxis_title='หมวดหมู่สินค้า',
    yaxis_title='จำนวนสินค้า',
    font=dict(
        family='Sarabun, sans-serif',
        size=11,
        color='black'
    )
)
    fig.update_traces(marker=dict(color='green', opacity=0.6, line=dict(color='red', width=1)), selector=dict(type='bar'))



    plot_div = fig.to_html(full_html=True)
    plot_divs = fig.to_html(full_html=True)
    plot_div2 = fig.to_html(full_html=True)
    return render(request, 'manager/dashboard.html', {'plot_div': plot_div, 'favorite_count':favorite_count(request),'plot_divs':plot_divs,'plot_div2':plot_div2})


@login_required(login_url='login')
@user_passes_test(manager_user,login_url='found_page')
def customer_orders(request):
    order = Order.objects.all().order_by('-order_date')
    return render(request,'manager/order_list.html',{'orders':order, 'favorite_count':favorite_count(request)})


# @login_required(login_url='login')
# def add_product(request):
#     form = ProductForm()
#     if request.method == 'POST':
#         form = ProductForm(request.POST,request.FILES)
#         if form.is_valid():
#             form.instance.user = request.user
#             form.save()
#             return redirect('product_list')
#         else:
#             form = ProductForm()
#     else:
#         form = ProductForm()
#     return render(request,'manager/add_product.html',{'form':form})

@login_required(login_url='login')
def add_product(request):
    m = Material.objects.all()

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
            return redirect('product_list')
    else:
        product_form = ProductForm()
        formset = ImageFormSet()
    
    return render(request, 'manager/add_product.html', {'product_form': product_form, 'formset': formset,'m':m})


@login_required(login_url='login')
def edit_product(request,id):
    product = Product.objects.get(pk=id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        else:
            form = ProductForm(instance=product)
    else:
        form = ProductForm(instance=product)
    return render(request,'manager/edit_product.html',{'form':form})



@login_required(login_url='login')
@user_passes_test(manager_user,login_url='found_page')
def delete_product(request,id):
    product = Product.objects.get(pk=id).delete()
    return redirect('product_list')

@login_required(login_url='login')
@user_passes_test(manager_user,login_url='found_page')
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


    return render(request, 'manager/order_detail.html',{
        'order':order,
        'qr_img_base64':qr_img_base64,
        'qr_img_base641':qr_img_base641,
        'deposit_price':int(deposit_price),
        'last_price':int(last_price),
        'forms':form,
        'forms2':form2,
        })


@login_required(login_url='login')
@user_passes_test(manager_user,login_url='found_page')
def material_list(request):
    m = Material.objects.all()
    paginator = Paginator(m, 5)
    page = request.GET.get('page', 1)  
    m = paginator.get_page(page)
    return render(request, 'manager/material.html',{'m':m})


@login_required(login_url='login')
@user_passes_test(manager_user,login_url='found_page')
def add_material(request):
    form = MaterialForm()
    if request.method == 'POST':
        form = MaterialForm(request.POST,request.FILES)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            return redirect('material_list')
        else:
            form = ProductForm()
    else:
        form = MaterialForm()
    return render(request,'manager/add_material.html',{'form':form})


def size_save(request):
    order =  Order.objects.all()
    return render(request,'manager/size_save.html',
    {
        'orders':order,
    })

def size_save_detail(request,id):
    order =  Order.objects.get(pk=id)
    m = MeasureSizeForm()
    if request.method == 'POST':
        m = MeasureSizeForm(request.POST, request.FILES)
        if m.is_valid():
            m.order = order
            m.save()
            return redirect(f'/manager/size_save_detail/{id}/')
        else:
            m = MeasureSizeForm(request.POST, request.FILES)
    return render(request,'manager/size_save_detail.html',
    {
        'orders':order,
        'form':m,
        'MeasureSize':MeasureSize.objects.filter(order=order),
    })

def add_size(request, id):
    order = get_object_or_404(Order, pk=id)
    if request.method == 'POST':
        h = request.POST.get('h', 0) 
        w = request.POST.get('w', 0) 
        d = request.POST.get('d', 0) 
        
        if h and w and d:
            measuresize = MeasureSize.objects.create(
                order=order,
                h=h,
                w=w,
                d=d,
            )
            measuresize.save()
            return redirect(f'/manager/size_save_detail/{id}/')

def get_size(request, id):
    measure_size = get_object_or_404(MeasureSize, pk=id)
    data = {
        'h': measure_size.h,
        'w': measure_size.w,
        'd': measure_size.d,
        'id':measure_size.id
    }
    return JsonResponse(data)

def delete_size(request, id,dlt):
    order = get_object_or_404(Order, pk=id)
    MeasureSize.objects.get(pk=dlt).delete()

    return redirect(f'/manager/size_save_detail/{id}/')

def edit_size(request, id,dlt):
    order =  Order.objects.get(pk=id)
    msz = MeasureSize.objects.get(pk=dlt)
    m = MeasureSizeForm(instance=msz)
    if request.method == 'POST':
        m = MeasureSizeForm(request.POST, request.FILES,instance=msz)
        if m.is_valid():
            m.save()
            return redirect(f'/manager/size_save_detail/{id}/')
        else:
            m = MeasureSizeForm(request.POST, request.FILES, instance=msz)
    return render(request,'manager/edit_size.html',
    {
        'orders':order,
        'form':m,

    })

    # size_save_detail/25/
# def edit_size(request, id,dlt):
#     order = get_object_or_404(Order, pk=id)
#     if request.method == 'POST':
#         h = request.POST.get('h', 0) 
#         w = request.POST.get('w', 0) 
#         d = request.POST.get('d', 0) 
        
#         if h and w and d:
#             measuresize = MeasureSize.objects.get(order=order,pk=dlt)
#             measuresize.h = h
#             measuresize.w = w
#             measuresize.d = d
#             measuresize.save()
#             return redirect(f'/manager/size_save_detail/{id}/')

def update_status(request,id,status):
    order = Order.objects.get(pk=id)
    order.status = status
    order.save()
    return redirect(f'/manager/order_detail/{id}/')
    

def upload_deposit(request, id):
    order = Order.objects.get(pk=id)
    
    if request.method == 'POST':
        form = DepositForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            if request.user.is_staff:
                return redirect(f'/manager/order_detail/{id}/')
            else:
                return redirect(f'/members/order/{id}/')

    else:
        form = DepositForm(instance=order)

def upload_payment(request, id):
    order = Order.objects.get(pk=id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            if request.user.is_staff:
                return redirect(f'/manager/order_detail/{id}/')
            else:
                return redirect(f'/members/order/{id}/')
    else:
        form = PaymentForm(instance=order)


def confirm_deposit(request,id):
    order = Order.objects.get(pk=id)
    order.deposit_payment = True
    order.save()
    return redirect(f'/manager/order_detail/{id}/')

def confirm_payment(request,id):
    order = Order.objects.get(pk=id)
    order.payment = True
    order.save()
    return redirect(f'/manager/order_detail/{id}/')

def cancel_order(request,id):
    if request.method == 'POST':
        choice = request.POST.get('choice')
        order = Order.objects.get(pk=id)
        order.status = 'ยกเลิก'
        order.save()
        cor = CancelOrder.objects.create(user=request.user,order=order,cancellation_reason=choice)
        cor.save()
        return redirect(f'/manager/order_detail/{id}/')

