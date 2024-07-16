from django.db import models
from django.contrib.auth.models import User
from manager.models import Product,Category,Material

class Favorite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

class Order(models.Model):
    PENDING = 'รอดำเนินการ'
    CONFIRM = 'ยืนยันคำสั่งซื้อ'
    IN_PROGRESS = 'ดำเนินการ'
    READY_FOR_SHIPPING = 'ติดตั้ง'
    COMPLETED = 'เสร็จสิ้น'
    CANCELLED = 'ยกเลิก'

    STATUS_CHOICES = [
        (PENDING, 'รอดำเนินการ'),
        (CONFIRM, 'ยืนยันคำสั่งซื้อ'),
        (IN_PROGRESS, 'ดำเนินการ'),
        (READY_FOR_SHIPPING, 'ติดตั้ง'),
        (COMPLETED, 'เสร็จสิ้น'),
        (CANCELLED, 'ยกเลิก'),
    ]

    staff = models.ForeignKey(User,on_delete=models.SET_NULL,limit_choices_to={'is_staff':True,'is_active':True,'is_superuser':False},null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='customer',null=True,blank=True)
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
    appt_date = models.DateField(null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    ship_date = models.DateField(null=True, blank=True)
    deposit = models.IntegerField(default=0)
    deposit_payment = models.BooleanField(default=False)
    deposit_proof = models.ImageField(upload_to='deposit_proofs/', blank=True, null=True)
    total_pay = models.IntegerField(default=0)
    payment = models.BooleanField(default=False)
    payment_proof = models.ImageField(upload_to='payment_proofs/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    image1 = models.ImageField(upload_to='install_proofs/',blank=True, null=True)
    image2 = models.ImageField(upload_to='install_proofs/',blank=True, null=True)
    image3 = models.ImageField(upload_to='install_proofs/',blank=True, null=True)
    image4 = models.ImageField(upload_to='install_proofs/',blank=True, null=True)


class MeasureSize(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='MeasureSize')
    h = models.FloatField(default=0)
    w = models.FloatField(default=0)
    d = models.FloatField(default=0)
    image1 = models.ImageField(upload_to='MeasureSize/', blank=True, null=True)
    image2 = models.ImageField(upload_to='MeasureSize/', blank=True, null=True)
    image3 = models.ImageField(upload_to='MeasureSize/', blank=True, null=True)
    image4 = models.ImageField(upload_to='MeasureSize/', blank=True, null=True)
    image5 = models.ImageField(upload_to='MeasureSize/', blank=True, null=True)
    image6 = models.ImageField(upload_to='MeasureSize/', blank=True, null=True)
    note = models.TextField(default='',null=True, blank=True)


class MeasureSizeMaterial(models.Model):
    measure_size = models.ForeignKey(MeasureSize, on_delete=models.CASCADE, related_name='measure_size_materials')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='material_measure_sizes')
    quantity = models.IntegerField()


class CancelOrder(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    cancellation_reason = models.CharField(max_length=100, blank=True, null=True)  



