from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.core.paginator import Paginator
from random import sample
from django.contrib import messages

from django.contrib.auth.decorators import login_required ,user_passes_test

from .context_processors import favorite_count


from manager.models import *
from members.models import *
from .forms import *

from .permissions import *


from linebot import LineBotApi
from linebot.models import TextSendMessage

LINE_CHANNEL_SECRET = '877bd53f1ac80e48fa046639090ee827'
LINE_ACCESS_TOKEN = 'aomFd5f2wOBWWUuzhS6kaVafX2MWzev8FdIpBnlRlRbg4/DrzbMG4heuCuiIbhKRBqYyM92KSZJ6fbiIWyjBqlwDpJZFz41hpc6lA3znUe3Bgu9XEmCO8bcH7kC28zVUUJcwxIjSDjcNjH19//Kx+AdB04t89/1O/w1cDnyilFU='
LIFF_URL = 'https://liff.line.me/2003676133-7Jnl1WK9'
LINE_LIFF_ID = '2003676133-7Jnl1WK9'

def send_line_message(user_id, message):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
    }
    data = {
        'to': user_id,
        'messages': [
            {
                'type': 'text',
                'text': message
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)

#ผูกบัญชี line
@login_required
def bind_line_user(req, user_id):
    user = req.user

    user.line_user_id = user_id
    user.save()

    message = f"ผูกบัญชีกับ Line สำเร็จ"
    send_line_message(user.line_user_id, message)
    messages.success(req, 'ผูกบัญชีกับ Line สำเร็จ')

    if req.is_superuser or req.is_staff and not req.is_active:
        return redirect('manager_dashboard') 
    else:
        return redirect('dashboard') 


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
                if user.is_superuser or user.is_staff and not user.is_active:
                    login(request, user)
                    return redirect('manager_dashboard') 
                else:
                    login(request, user)
                    return redirect('dashboard')  

        else:
            form = LoginForm()
    else:
        form = LoginForm()

    return render(request,'login.html',{'form':form })


@login_required(login_url='login')
def sign_out(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    return render(request,'profile.html' ,{'favorite_count':favorite_count(request)})


@login_required(login_url='login')
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


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'change_password.html', {'form': form ,'favorite_count':favorite_count(request)})


@login_required(login_url='login')
def delete_user(request):
    User.objects.get(username=request.user).delete()
    return redirect('login')


@login_required(login_url='login')
@user_passes_test(members_user,login_url='found_page')
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

@login_required(login_url='login')
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


