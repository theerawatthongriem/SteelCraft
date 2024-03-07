from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE ,null=True ,blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=500)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='meterial/')

    def __str__(self):
        return self.name