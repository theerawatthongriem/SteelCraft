from django.shortcuts import render,redirect,get_object_or_404 

from members.models import Order,MeasureSize
from .forms import *
from base_app.context_processors import favorite_count
from django.contrib.auth.decorators import user_passes_test,login_required

from django.db.models import Count, OuterRef, Subquery, IntegerField
from django.db.models.functions import Coalesce
from django.http import JsonResponse,HttpResponseRedirect
from django.forms import formset_factory

from django.db.models.functions import TruncMonth, TruncYear
import plotly.graph_objs as go
from django.db.models import Sum,F
import pandas as pd

import plotly.express as px
import plotly.io as pio
from collections import defaultdict

import io
import locale

from .permissions import *

from promptpay import qrcode
from members.models import *

from django.core.paginator import Paginator

import base64,urllib
from io import BytesIO

from datetime import date

import json


@login_required(login_url='login')
@user_passes_test(manager_user,login_url='found_page')
def manager_dashboard(request):
    orders = Order.objects.all().exclude(status__in=['เสร็จสิ้น', 'ยกเลิก'])

    for order in orders:
        order.days_until_ship = (order.ship_date - date.today()).days
    return render(request, 'manager/dashboard.html', {'orders':orders})


@login_required(login_url='login')
@user_passes_test(manager_user,login_url='found_page')
def overwiew(request):

    month_names = {
        1: 'มกราคม', 2: 'กุมภาพันธ์', 3: 'มีนาคม', 4: 'เมษายน',
        5: 'พฤษภาคม', 6: 'มิถุนายน', 7: 'กรกฎาคม', 8: 'สิงหาคม',
        9: 'กันยายน', 10: 'ตุลาคม', 11: 'พฤศจิกายน', 12: 'ธันวาคม'
    }


    if request.method == 'POST':
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            year = int(form.cleaned_data['year'])
            month = int(form.cleaned_data['month'])
    else:
        form = DateSelectionForm()
        year = datetime.now().year
        month = datetime.now().month

    sales_data = (
        Order.objects
        .annotate(year=TruncYear('order_date'), month=TruncMonth('order_date'))
        .values('year', 'month', 'product_category__name')
        .annotate(total_sales=Sum(F('price') * F('quantity')))
        .order_by('year', 'month', 'product_category__name')
    )

    sales_by_month_year = defaultdict(lambda: defaultdict(int))

    for entry in sales_data:
        year_month = (entry['year'].year, entry['month'].month)
        category = entry['product_category__name']
        sales_by_month_year[year_month][category] += entry['total_sales']

    data = sales_by_month_year.get((year, month), {})
    labels = list(data.keys())
    sizes = list(data.values())


    if data:
        fig = px.pie(values=sizes, names=labels)
        # chart_html = pio.to_html(fig, full_html=False)
    else:
        fig = px.pie(values=sizes, names=labels,title='ไม่มียอดขายในเดือนนี้')
        # chart_html = pio.to_html(fig, full_html=False)

    fig.update_layout(
        title_font=dict(size=16, family='Noto Sans Thai, sans-serif', color='black'),
        font=dict(family="Noto Sans Thai, sans-serif", size=16, color="black")
    )

    chart_html = pio.to_html(fig, full_html=True)

    print(month)
    
    t = []
    
    for i in Order.objects.all():
        t.append(i.total_price)
    tsum = sum(t)

    members = User.objects.filter(is_active=True,is_staff=False,is_superuser=False).count()
    staff = User.objects.filter(is_active=True,is_staff=True,is_superuser=False).count()
    superuser = User.objects.filter(is_active=True,is_staff=True,is_superuser=True).count()

     # สร้าง Bar Chart โดยใช้ Plotly

    sales_data_total = Order.objects.values('product_category__name').annotate(total_sales=Sum('total_price'))
    labels_total = [entry['product_category__name'] for entry in sales_data_total]
    sizes_total = [entry['total_sales'] for entry in sales_data_total]

    fig_bar = px.bar(x=labels_total, y=sizes_total, title='ยอดขายตามหมวดหมู่', labels={'x': 'หมวดหมู่', 'y': 'ยอดขาย'})
    fig_bar.update_layout(
        title_font=dict(size=16, family='Noto Sans Thai, sans-serif', color='black'),
        font=dict(family="Noto Sans Thai, sans-serif", size=14, color="black")
    )
    chart_bar_html = pio.to_html(fig_bar, full_html=False)


    return render(request, 'manager/overview.html', {
        'form': form, 
        'chart_html': chart_html, 
        'chart_bar_html': chart_bar_html, 
        'year': year, 
        'month': month_names[month],
        't':tsum,
        'members':members,
        'staff':staff,
        'superuser':superuser,
        })



@login_required(login_url='login')
@user_passes_test(manager_user,login_url='found_page')
def customer_orders(request):

    order_status = Order.objects.first()


    order = Order.objects.all().order_by('-order_date')

    paginator = Paginator(order, 8)
    page = request.GET.get('page', 1)  
    order = paginator.get_page(page)
    
    return render(request,'manager/order_list.html',{'orders':order, 'favorite_count':favorite_count(request),'order_status':order_status})

@login_required(login_url='login')
@user_passes_test(manager_user,login_url='found_page')
def customer_orders_category(request,status):

    order_status = Order.objects.first()

    order = Order.objects.filter(status=status).order_by('-order_date')

    paginator = Paginator(order, 8)
    page = request.GET.get('page', 1)  
    order = paginator.get_page(page)
    
    return render(request,'manager/order_list_category.html',{
        'orders':order, 
        'favorite_count':favorite_count(request),
        'order_status':order_status,
        'status':status,
    })


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
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_category')
        else:
            form = CategoryForm()
    else:
        form = CategoryForm()
    return render(request,'manager/add_category.html',{'category_form':form,'category':Category.objects.all()})

@login_required(login_url='login')
def edit_category(request,id,action):
    category = Category.objects.get(pk=id)
    if action == 'delete':
        category.delete()
        return redirect('add_category')
    elif action == 'update':
        form = CategoryForm()
        if request.method == 'POST':
            form = CategoryForm(request.POST,instance=category)
            if form.is_valid():
                form.save()
                return redirect('add_category')
            else:
                form = CategoryForm(instance=category)
        else:
            form = CategoryForm(instance=category)
    return render(request,'manager/add_category.html',{'category_form':form,'category':Category.objects.all(),'action':action})

@login_required(login_url='login')
def update_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    ImageFormSet = formset_factory(EditProductImageForm, extra=3)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        formset = ImageFormSet(request.POST, request.FILES)
        if product_form.is_valid() and formset.is_valid():
            product_form.save()
            for form in formset:
                image = form.cleaned_data.get('image')
                if image:
                    ProductImage.objects.create(product=product, image=image)
            return redirect('product_list')
    else:
        product_form = ProductForm(instance=product)
        formset = ImageFormSet()

    existing_images = ProductImage.objects.filter(product=product)

    return render(request, 'manager/update_product.html', {
        'product_form': product_form,
        'formset': formset,
        'product': product,
        'existing_images': existing_images,
    })

def delete_image(request, image_id):
    image = get_object_or_404(ProductImage, id=image_id)
    product_id = image.product.id
    image.delete()
    return redirect('update_product', product_id=product_id)


@login_required(login_url='login')
@user_passes_test(manager_user,login_url='found_page')
def delete_product(request,id):
    product = Product.objects.get(pk=id).delete()
    return redirect('product_list')

@login_required(login_url='login')
@user_passes_test(manager_user,login_url='found_page')
def order_detail(request,id):

    order = Order.objects.get(pk=id)


    form3 = OrderForm(instance=order)

    id_or_phone_number = "0956452530"
    amount = order.total_price

    

    deposit_price = order.total_price * (order.deposit)/100
    last_price = order.total_price - deposit_price
    order.total_pay = last_price
    order.save()

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
    form4 = OrderInstallProofsForm(instance=order)

    print(order.deposit_payment)


    return render(request, 'manager/order_detail.html',{
        'order':order,
        'qr_img_base64':qr_img_base64,
        'qr_img_base641':qr_img_base641,
        'deposit_price':int(deposit_price),
        'last_price':int(order.total_pay),
        'forms':form,
        'forms2':form2,
        'forms3':form3,
        'forms4':form4,
        })

@login_required(login_url='login')
def edit_order(request,id):
    order = Order.objects.get(pk=id)
    if request.method == 'POST':
        forms3 = OrderForm(request.POST,instance=order)
        if forms3.is_valid():
            forms3.save(commit=False).staff = order.staff
            forms3.save()
            return redirect(f'/manager/order_detail/{id}/')
        else:
            forms3 = OrderForm(instance=order)
    else:
        forms3 = OrderForm(instance=order)

def order_install_proofs(request,id):
    order = Order.objects.get(pk=id)
    if request.method == 'POST':
        form4 = OrderInstallProofsForm(request.POST,request.FILES,instance=order)
        if form4.is_valid():
            form4.save()
            return redirect(f'/manager/order_detail/{id}/')
    else:
        form4 = OrderInstallProofsForm(instance=order)


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

@login_required(login_url='login')
@user_passes_test(manager_user,login_url='found_page')
def update_material(request,id,action):
    m = Material.objects.get(pk=id)

    if action == 'delete':
        m.delete()
        return redirect('material_list')
        
        
    elif action == 'update':
        form = MaterialForm(instance=m)
        if request.method == 'POST':
            form = MaterialForm(request.POST,request.FILES,instance=m)
            form.instance.user = request.user
            if form.is_valid():
                form.save()
                return redirect('material_list')
            else:
                form = ProductForm(instance=m)
        else:
            form = MaterialForm(instance=m)
    
    return render(request,'manager/update_material.html',{'form':form})


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

def delete_size(request, id,dlt):
    order = get_object_or_404(Order, pk=id)
    MeasureSize.objects.get(pk=dlt).delete()

    return redirect(f'/manager/size_save_detail/{id}/')

def edit_size(request, id,dlt,q):
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
        'q':q,

    })

@login_required(login_url='login')
def measure_size_detail(request, measure_size_id, q):
    measure_size = get_object_or_404(MeasureSize, pk=measure_size_id)
    
    if request.method == 'POST':
        material_form = MeasureSizeMaterialForm(request.POST)
        if material_form.is_valid():
            # Check if material already exists for the given measure size
            material_data = material_form.cleaned_data
            if not MeasureSizeMaterial.objects.filter(measure_size=measure_size, material=material_data['material']).exists():
                measure_size_material = material_form.save(commit=False)
                measure_size_material.measure_size = measure_size
                measure_size_material.save()
                material_form = MeasureSizeMaterialForm()  # Reset form after successful save
                return HttpResponseRedirect(request.path)  # Redirect back to the same page after successful save
            else:
                # Material already exists, redirect back to the same page with an error message
                return HttpResponseRedirect(request.path)  # Redirect back to the same page
    else:
        material_form = MeasureSizeMaterialForm()
    
    return render(request, 'manager/measure_size_detail.html', {
        'measure_size': measure_size,
        'form': material_form,
        'q': q,
    })

def update_status(request,id,status):
    order = Order.objects.get(pk=id)
    order.status = status
    
    if status == 'ดำเนินการ':
        material_stock(request,order=order)

    order.save()
    return redirect(f'/manager/order_detail/{id}/')
    
def material_stock(request, order):
    materials = Material.objects.all()
    measure_sizes = MeasureSize.objects.filter(order=order)

    for measure_size in measure_sizes:
        measure_size_materials = MeasureSizeMaterial.objects.filter(measure_size=measure_size)
        for measure_size_material in measure_size_materials:
            material = measure_size_material.material
            quantity = measure_size_material.quantity

            # Update material stock
            material.quantity -= quantity
            material.save()

@login_required(login_url='login')
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

@login_required(login_url='login')
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
        cor = CancelOrder.objects.create(user=request.user,
        order=order,
        cancellation_reason=choice)
        cor.save()
        return redirect(f'/manager/order_detail/{id}/')


def material_order(request):
    order = Order.objects.filter(status='ยืนยันคำสั่งซื้อ')
    for i in order:
        print(i)
        for o in i.MeasureSize.all():
            print(o)
            for l in o.measure_size_materials.all():
                print(l.material ,i.quantity)

    return render(request,'manager/material_order.html',{'order':order})

@login_required(login_url='login')
def staff_manager(request):
    user = User.objects.filter(is_staff=True,is_superuser=False,is_active=True)

    paginator = Paginator(user, 8)
    page = request.GET.get('page', 1)  
    user = paginator.get_page(page)

    form = AddStaffForm()
    if request.method == 'POST':
        form = AddStaffForm(request.POST)
        if form.is_valid():
            form.save(commit=False).is_staff = True
            form.save(commit=False).is_active = True
            form.save()
            return redirect('staff_manager')
        else:
            form = AddStaffForm()
    else:
        form = AddStaffForm()
        
    return render(request,'manager/staff_manager.html',{
        'staff':user,'form':form
        })

@login_required(login_url='login')
def edit_staff_manager(request,id):

    user = User.objects.get(pk=id)

    form = EditStaffForm(instance=user)
    if request.method == 'POST':
        form = EditStaffForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('staff_manager')
        else:
            form = EditStaffForm(instance=user)
    else:
        form = EditStaffForm(instance=user)
        
    return render(request,'manager/edit_staff_manager.html',{
        'form':form
        })

@login_required(login_url='login')
def delete_staff(request,id):
    user = User.objects.get(pk=id).delete()
    return redirect('staff_manager')


def add_working_day(request):
    if request.method == 'POST':
        form = WorkingDayForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_working_day')  # เปลี่ยนเส้นทางกลับไปยังหน้าฟอร์มหลังจากบันทึก
    else:
        form = WorkingDayForm()

    working_days = list(WorkingDay.objects.all().values('date_work'))
    for day in working_days:
        day['date_work'] = day['date_work'].isoformat()
    
    context = {
        'form': form,
        'working_days': json.dumps(working_days),
    }
    return render(request, 'manager/add_working_day.html', context)

def delete_working_day(request, date_work):
    date = WorkingDay.objects.filter(date_work=date_work)
    date.delete()
    return redirect('add_working_day')
    


