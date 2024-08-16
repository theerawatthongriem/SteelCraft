from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.core.paginator import Paginator
from random import sample
from django.contrib import messages

from django.contrib.auth.models import User


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

from django.http import JsonResponse
import requests


from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy

class ForgotPasswordView(PasswordResetView):
    template_name = 'forgot_password.html'
    email_template_name = 'forgot_password_email.html'
    success_url = reverse_lazy('login')  

class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'reset_password_confirm.html'
    success_url = reverse_lazy('login') 


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
        order_status = Order.objects.filter(user=user_msg.user).exclude(status='ยกเลิก')
        print(order_status)

        if order_status:
            for i in order_status:
                order_user = f'คำสั่งซื้อที่ {i.id} \nลูกค้า คุณ {i.first_name} {i.last_name}'
                order_product = f'\n\nสินค้า : {i.product.name} \n'
                order_price = f'ราคา {int(i.product.price):,} บาท \n'
                order_qty = f'จำนวน {i.quantity} รายการ \n'
                order_total_price = f'ราคารวม {int(i.total_price):,} บาท'
                order_state = f'\n\n สถานะ : {i.status}'
                
                text_msg =  (order_user + order_product + order_qty + order_price
                + order_total_price + order_state)
                send_line_message(user_id, message=text_msg)
        else:
            text_msg = 'ไม่พบคำสั่งซื้อ'
            send_line_message(user_id, message=text_msg)
    if text == 'ติดต่อเจ้าหน้าที่':  # รับ user_id ของผู้ส่งข้อความ
        text_msg = 'รอเจ้าหน้าที่ตอบกลับ'
        send_line_message(user_id, message=text_msg)


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

@login_required(login_url='login')
def connect_line_user(request):
    if request.method == 'POST':
        data = request.POST.get('userId')
        check = UserMessage.objects.filter(user=request.user).first()
        if check is None:
            UserMessage.objects.create(user=request.user, line_id=data)
            message = f'{request.user} {request.user.first_name} {request.user.last_name} \n เชื่อมต่อบัญชีไลน์เรียบร้อย ครับ/ค่ะ'
            # You might want to add some logic here to display the message
        else:
            return redirect('dashboard')
            
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

@login_required(login_url='login')
def line(request):
    return render(request,'line.html')

def home(request):
    users = User.objects.filter(is_staff=True) | User.objects.filter(is_superuser=True)
    products = Product.objects.filter(user__in=users)
    return render(request,'home.html',{
        'products':products,
        'favorite_count':favorite_count(request)
        })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
    else:
        form = RegisterForm()
        profile_form = UserProfileForm()

    return render(request, 'register.html', {'form': form, 'profile_form': profile_form})

def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user:
                if user.is_superuser:
                    login(request, user)
                    return redirect('manager_dashboard') 
                elif user.is_staff:
                    login(request, user)
                    return redirect('staff_dashboard') 
                else:
                    login(request, user)
                    return redirect('dashboard')  
            else:
                form.add_error(None, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    
    return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
def sign_out(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    return render(request,'profile.html' ,{'favorite_count':favorite_count(request)})

@login_required(login_url='login')
def editprofile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = EditForm(request.POST, instance=user)
        userprofile_form = UserProfileForm(request.POST, instance=user_profile)
        
        if form.is_valid() and userprofile_form.is_valid():
            form.save()
            userprofile_form.save()
            return redirect('profile')
    else:
        form = EditForm(instance=user)
        userprofile_form = UserProfileForm(instance=user_profile)

    return render(request,'editprofile.html',{
        'form':form ,'userprofile':userprofile_form ,
        'favorite_count':favorite_count(request)})

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
    category = Category.objects.all()
    users = User.objects.filter(is_staff=True) | User.objects.filter(is_superuser=True)
    products = Product.objects.filter(user__in=users)
    paginator = Paginator(products, 8)
    page = request.GET.get('page', 1)  
    products = paginator.get_page(page)
    return render(request, 'product_list.html', {
        'products': products ,
        'favorite_count':favorite_count(request),
        'cate':category
        })

def product_category(request,cate):
    category = Category.objects.get(id=cate)
    users = User.objects.filter(is_staff=True) | User.objects.filter(is_superuser=True)
    products = Product.objects.filter(user__in=users,category=category.id)
    paginator = Paginator(products, 8)
    page = request.GET.get('page', 1)  
    products = paginator.get_page(page)
    return render(request, 'product_category.html', {'products': products ,'favorite_count':favorite_count(request),'cate':category})

def product_members(request):
    
    products = Product.objects.filter(user=request.user)
    paginator = Paginator(products, 8)
    page = request.GET.get('page', 1)  
    products = paginator.get_page(page)
    return render(request, 'members/product_members.html', {'products': products ,'favorite_count':favorite_count(request)})

def product_detail(request,id):
    products = Product.objects.get(pk=id)
    return render(request, 'product_detail.html', {'products': products})

@login_required(login_url='login')
def found_page(request):
    return render(request,'found_page.html')




