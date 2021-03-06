from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profile1.png", upload_to="Profile/", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Category(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.ForeignKey(Category, max_length=200, null=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(
        Customer,  null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product,  null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'Name: {str(self.customer)}, Product: {str(self.product.name)}'

