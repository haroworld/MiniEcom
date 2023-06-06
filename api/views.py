from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import generics
import datetime
from .serializers import *
from store.models import *


@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET':'/api/products'},
        {'GET': '/api/products/id'},
        {'GET': '/api/cart'},
        {'POST': '/api/update_item'},
        {'POST': '/api/process_order'},

        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},


        
    ]
    return Response(routes)

@api_view(['GET'])
def getProducts(request):
    products = Products.objects.all()
    serializer = ProductSerializers(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    product = Products.objects.get(id=pk)
    serializer = ProductSerializers(product, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCart(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, completed = False)
    items = order.orderitem_set.all()
    serializer = OrderItemsSerializers(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateItem(request):
    data = request.data
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

    serializer = OrderItemsSerializers(orderItem, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = request.data
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        total = float(data['total'])
        order.order_id = transaction_id

        if total == float(order.get_order_total):
            order.completed = True
        order.save()

        ShippingAdress.objects.create(
            customer = customer,
            order=order,
            address=data['address'],
            city=data['city'],
            state=data['state'],
            zipcode=data['zipcode'],
        )

    shippingAdress = ShippingAdress.objects.get(customer=customer, order=order)

    serializer = ProcessOrderSerializers(shippingAdress, many=False)
    return Response(serializer.data)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
