from django.shortcuts import render
from members.models import Order
from django.core.paginator import Paginator
from .forms import OrderForm

# Create your views here.
def staff_dashboard(request):
    return render(request,'staff/dashboard.html')

def staff_order_list(request):

    order_status = Order.objects.first()


    order = Order.objects.filter(staff=request.user).order_by('-order_date')

    paginator = Paginator(order, 8)
    page = request.GET.get('page', 1)  
    order = paginator.get_page(page)
    
    return render(request,'staff/order_list.html',{'orders':order,'order_status':order_status})

def staff_orders_category(request,status):

    order_status = Order.objects.first()

    order = Order.objects.filter(status=status,staff=request.user).order_by('-order_date')

    paginator = Paginator(order, 8)
    page = request.GET.get('page', 1)  
    order = paginator.get_page(page)
    
    return render(request,'staff/order_list_category.html',{
        'orders':order, 
        'order_status':order_status,
        'status':status,
    })

def staff_size_save(request):
    order =  Order.objects.filter(staff=request.user)
    return render(request,'staff/size_save.html',
    {
        'orders':order,
    })

def staff_edit_order(request,id):
    order = Order.objects.get(pk=id)
    if request.method == 'POST':
        forms3 = OrderForm(request.POST,instance=order)
        if forms3.is_valid():
            forms3.save()
            return redirect(f'/manager/order_detail/{id}/')
        else:
            forms3 = OrderForm(instance=order)
    else:
        forms3 = OrderForm(instance=order)
