from django.db import models
from django.contrib.auth.models import User
from manager.models import Product,Category

class Favorite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

class Order(models.Model):
    PENDING = 'รอดำเนินการ'
    CONFIRM = 'ยืนยันคำสั่งซื้อ'
    MEASURING = 'นัดวัดขนาด'
    MATERIAL_SELECTION = 'เลือกวัสดุ'
    IN_PROGRESS = 'ดำเนินการ'
    READY_FOR_SHIPPING = 'พร้อมติดตั้ง'
    INSTALLATION = 'ติดตั้ง'
    COMPLETED = 'เสร็จสิ้น'
    CANCELLED = 'ยกเลิก'

    STATUS_CHOICES = [
        (PENDING, 'รอดำเนินการ'),
        (CONFIRM, 'ยืนยันคำสั่งซื้อ'),
        (MEASURING, 'นัดวัดขนาด'),
        (MATERIAL_SELECTION, 'เลือกวัสดุ'),
        (IN_PROGRESS, 'ดำเนินการ'),
        (READY_FOR_SHIPPING, 'พร้อมติดตั้ง'),
        (INSTALLATION, 'ติดตั้ง'),
        (COMPLETED, 'เสร็จสิ้น'),
        (CANCELLED, 'ยกเลิก'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    address = models.TextField()
    delivery_location = models.CharField(max_length=500 ,null=True, blank=True)
    phone_number = models.CharField(max_length=15,default='')
    note = models.TextField(default='',null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    ship_date = models.DateTimeField(null=True, blank=True)
    payment = models.BooleanField(default=False)
    payment_proof = models.ImageField(upload_to='payment_proofs/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)








