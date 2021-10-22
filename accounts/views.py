from django.shortcuts import render
from .models import *


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    panding = orders.filter(status="Pending").count()

    contaxt = {
        'orders': orders,
        'customers':customers,
        'total_orders':total_orders,
        'delivered':delivered,
        'panding':panding

    }
    return render(request, 'accounts/dashboard.html', contaxt)


def products(request):
    products = Product.objects.all()
    contaxt = {
        'products': products
    }
    return render(request, 'accounts/products.html', contaxt)


def customer(request):
    return render(request, 'accounts/customers.html')
