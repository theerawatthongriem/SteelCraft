from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.core.paginator import Paginator
from random import sample
from django.contrib import messages

from django.contrib.auth.decorators import login_required ,user_passes_test

from .context_processors import favorite_count

from .models import *
from manager.models import *
from members.models import *
from .forms import *

from .permissions import *

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST,require_GET
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,ImageSendMessage

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests



LINE_CHANNEL_SECRET = 'c1d5e281953c8e81cf8b80c4c0230f1a'
LINE_ACCESS_TOKEN = '6heBocJbWYV6wSyCfNuoO57PPhLeCOBbgV2GGZY1ta5LDqveoj/R+nGoSMViOWBJpMYxZMTrE6IvfdCHMyzYZfQwUkuWf0ILXs3MrLmuKHyYFOex7B77oGMFl1h8jRwfuL3ug5E1t+SvlyIaKgts7AdB04t89/1O/w1cDnyilFU='
LIFF_URL = 'https://liff.line.me/2003837170-ZVz5KK9o'
LINE_LIFF_ID = '2003837170-ZVz5KK9o'


line_bot_api = LineBotApi('6heBocJbWYV6wSyCfNuoO57PPhLeCOBbgV2GGZY1ta5LDqveoj/R+nGoSMViOWBJpMYxZMTrE6IvfdCHMyzYZfQwUkuWf0ILXs3MrLmuKHyYFOex7B77oGMFl1h8jRwfuL3ug5E1t+SvlyIaKgts7AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('15dc965632146d675d1bcd231f6cfeeb')

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        signature = request.headers.get('X-Line-Signature', '')
        body = request.body.decode('utf-8')
        
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseBadRequest()

        return HttpResponse(status=200)
    else:
        return HttpResponse("Method Not Allowed", status=405)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    # print("Received message:", text)  # แสดงข้อความในคอนโซล
    user_id = event.source.user_id
    if text == 'ติดตามสถานะ':  # รับ user_id ของผู้ส่งข้อความ
        print("From user ID:", user_id)  # แสดง us
        user_msg = UserMessage.objects.get(line_id=user_id)
        order_status = Order.objects.filter(user=user_msg.user)
        print(order_status)

        for i in order_status:
            img_url = f'https://0734-202-176-130-25.ngrok-free.app'+i.product.image.url 
            text_msg = f'คำสั่งซื้อที่ {i.id} ผู้ใช้ {i.user} \n คุณ {i.first_name} {i.last_name}' + f'\n\n {i.product.name} ราคา {i.product.price} จำนวน {i.quantity} รายการ \n ราคารวม {float(i.total_price)} \n\n สถานะ : {i.status}' + '\n\n' 'ดูเพิ่มเติม คลิก : ' + f'https://2736-202-176-131-45.ngrok-free.app/members/order_detail/{i.id}/'
            send_line_message(user_id, message=text_msg ,image_url=img_url)

# def send_line_message(user_id, message):
#     url = 'https://api.line.me/v2/bot/message/push'
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
#     }
#     data = {
#         'to': user_id,
#         'messages': [
#             {
#                 'type': 'text',
#                 'text': message
#             }
#         ]
#     }
#     response = requests.post(url, headers=headers, json=data)

def send_line_message(user_id, message, image_url):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
    }
    text = {
                'type': 'text',
                'text': message
            }

    img = {
                'type': 'image',
                'originalContentUrl': image_url,
                'previewImageUrl': image_url
            }

    data = {
            'to': user_id,
            'messages': [
                text,
                img
            ]
        }

    response = requests.post(url, headers=headers, json=data)

@login_required(login_url='login')
def connect_line_user(request):
    if request.method == 'POST':
        data = request.POST.get('userId')
        check = UserMessage.objects.filter(user=request.user)
        if check is not None:
            message = f'{request.user} {request.user.first_name} {request.user.last_name} \n เคยผูกบัญชีไว้แล้ว ครับ/ค่ะ'
        else:
            UserMessage.objects.create(user=request.user, line_id=data)
            message = f'{request.user} {request.user.first_name} {request.user.last_name} \n เชื่อมต่อบัญชีไลน์เรียบร้อย ครับ/ค่ะ'
        url = 'https://api.line.me/v2/bot/message/push'
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
        }

        text = {
                'type': 'text',
                'text': message
            }

        datas = {
            'to': data,
            'messages': [
                text,
            ]
        }

        response = requests.post(url, headers=headers, json=datas)
        if request.user.is_staff and request.user.is_superuser:
            return redirect('manager_dashboard')
        else:
            return redirect('dashboard')

def line(request):
    return render(request,'line.html')

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


