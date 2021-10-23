from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import *
from .forms import *
from .filter import *
from .decorators import *


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user)
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)




@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username Or password is incorrect')
    context = {

    }
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    panding = orders.filter(status="Pending").count()

    contaxt = {
        'orders': orders,
        'customers': customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'panding': panding,

    }
    return render(request, 'accounts/dashboard.html', contaxt)

@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    panding = orders.filter(status="Pending").count()
    context = {
        'orders':orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'panding': panding
    }
    return render(request, 'accounts/user.html', context)

@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('user-page')
            
    contaxt = {
        'form':form,
    }
    return render(request, 'accounts/account_settings.html', contaxt)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    contaxt = {
        'products': products
    }
    return render(request, 'accounts/products.html', contaxt)

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    contaxt = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'myFilter': myFilter
    }
    return render(request, 'accounts/customers.html', contaxt)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = UpdateCustomerForm(instance=customer)
    if request.method == "POST":
        form = UpdateCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('home')
    contaxt = {
        'form': form
    }
    return render(request, 'accounts/update_customer.html', contaxt)



@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')
    contaxt = {
        'formset': formset,
    }
    return render(request, 'accounts/order_form.html', contaxt)

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = orderForm(instance=order)

    if request.method == "POST":
        form = orderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')
    contaxt = {
        'form': form
    }
    return render(request, 'accounts/update_order_form.html', contaxt)

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('home')
    contaxt = {
        'order': order
    }
    return render(request, 'accounts/delete.html', contaxt)
