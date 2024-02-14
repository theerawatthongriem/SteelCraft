from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.core.paginator import Paginator
from random import sample
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .context_processors import favorite_count


from manager.models import *
from members.models import *
from .forms import *




def home(request):

    products = Product.objects.all()
    return render(request,'home.html',{'products':products,'favorite_count':favorite_count(request)})

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            form = RegisterForm()
    else:
        form = RegisterForm()
    return render(request,'register.html',{'form':form })


def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username,password=password)
            if user:
                login(request,user)
                next_path = request.GET.get('next', '/')
                return redirect(next_path)
        else:
            form = LoginForm()
    else:
        form = LoginForm()

    return render(request,'login.html',{'form':form })

def sign_out(request):
    logout(request)
    return redirect('login')


def profile(request):
    return render(request,'profile.html' ,{'favorite_count':favorite_count(request)})


def editprofile(request):
    form = EditForm(instance=request.user)
    if request.method == 'POST':
        form = EditForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            form = EditForm()
    else:
        form = EditForm(instance=request.user)

    return render(request,'editprofile.html',{'form':form ,'favorite_count':favorite_count(request)})


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'change_password.html', {'form': form ,'favorite_count':favorite_count(request)})

def delete_user(request):
    User.objects.get(username=request.user).delete()
    return redirect('login')

def dashboard(request):
    return render(request,'members/dashboard.html',{'favorite_count':favorite_count(request)})


def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 8)
    page = request.GET.get('page', 1)  
    products = paginator.get_page(page)
    return render(request, 'product_list.html', {'products': products ,'favorite_count':favorite_count(request)})

def product_detail(request,id):
    product = list(Product.objects.all())
    if len(product) >= 8:
        random_products = sample(list(product), 5)
    else:
        random_products = product    
    
    products = Product.objects.get(pk=id)
    favorite = Favorite.objects.filter(user=request.user)
    for i in favorite:
        if i.product.id == id:
            favorite = id
        else:
            favorite = ''
    return render(request, 'product_detail.html', {'products': products,'product':random_products,'favorite':favorite, 'favorite_count':favorite_count(request)})


def found_page(request):
    return render(request,'found_page.html')



# def search_view(request):
#     all_people = User.objects.all()
#     context = {'count': all_people.count()}
#     return render(request, 'search.html', context)


# def search_results_view(request):
#     query = request.GET.get('search', '')
#     print(f'{query = }')

#     all_people = User.objects.all()
#     if query:
#         people = all_people.filter(username__icontains=query)
#     else:
#         people = []

#     context = {'people': people, 'count': all_people.count()}
#     return render(request, 'search_results.html', context)
    