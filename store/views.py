from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib import messages
import json
import datetime
from .models import *



# Create your views here.

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('store')
    

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exits')

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, 'Username or password is not correct')

    return render(request, 'store/login.html')

def Logout(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')


            login(request, user)
            Customer.objects.create(
                user = request.user,
                name = user.first_name,
                email = user.email
            )
            return redirect('store')

        else:
            messages.success(
                request, 'An error has occurred during registration')

    
    context = {'form': form}
    return render(request, 'store/register.html', context)


def store(request):
    products = Products.objects.all()
    context = {"products":products}
    return render(request, 'store/store.html', context)

def viewProduct(request, pk):
    product = Products.objects.get(id=pk)
    context = {'product':product}
    return render(request, 'store/view_product.html', context)

def cart(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, completed = False)
    items = order.orderitem_set.all()
    context = {'items':items, 'order':order}
    return render(request, 'store/order.html', context)


def checkout(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, completed = False)
    items = order.orderitem_set.all()
    context = {'items':items, 'order':order}
    return render(request, 'store/order_checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Products.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        total = float(data['form']['total'])
        order.order_id = transaction_id

        if total == float(order.get_order_total):
            order.completed = True
        order.save()

        ShippingAdress.objects.create(
            customer = customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    
    return JsonResponse('payment complete', safe=False)



