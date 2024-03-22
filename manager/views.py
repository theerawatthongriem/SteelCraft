from django.shortcuts import render,redirect,get_object_or_404
from members.models import Order,MeasureSize
from .forms import *
from base_app.context_processors import favorite_count
from django.contrib.auth.decorators import user_passes_test,login_required

from django.db.models import Count, OuterRef, Subquery, IntegerField
from django.db.models.functions import Coalesce
from django.http import JsonResponse


import plotly.graph_objs as go

from .permissions import *

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
    order = Order.objects.all()
    return render(request,'manager/order_list.html',{'orders':order, 'favorite_count':favorite_count(request)})


@login_required(login_url='login')
def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('product_list')
        else:
            form = ProductForm()
    else:
        form = ProductForm()
    return render(request,'manager/add_product.html',{'form':form})


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
    return render(request, 'manager/order_detail.html',{'order':order})

@login_required(login_url='login')
@user_passes_test(manager_user,login_url='found_page')
def material_list(request):
    m = Material.objects.all()
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
    return render(request,'manager/size_save_detail.html',
    {
        'orders':order,
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
    order = get_object_or_404(Order, pk=id)
    if request.method == 'POST':
        h = request.POST.get('h', 0) 
        w = request.POST.get('w', 0) 
        d = request.POST.get('d', 0) 
        
        if h and w and d:
            measuresize = MeasureSize.objects.get(order=order,pk=dlt)
            measuresize.h = h
            measuresize.w = w
            measuresize.d = d
            measuresize.save()
            return redirect(f'/manager/size_save_detail/{id}/')

