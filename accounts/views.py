from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import *
from .forms import *
from .filter import *

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


def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    contaxt = {
        'customer': customer,
        'orders':orders,
        'order_count':order_count,
        'myFilter':myFilter
    }
    return render(request, 'accounts/customers.html', contaxt)


def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5 )
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')
    contaxt = {
        'formset':formset,
    }
    return render(request, 'accounts/order_form.html', contaxt)

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = orderForm(instance=order)

    if request.method == "POST":
        form = orderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')
    contaxt = {
        'form':form
    }
    return render(request, 'accounts/update_order_form.html', contaxt)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('home')
    contaxt = {
        'order':order
    }
    return render(request, 'accounts/delete.html', contaxt)