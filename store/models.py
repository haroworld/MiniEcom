from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    category = models.ForeignKey(Categories,on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_orderd = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False, null=True, blank=True)
    order_id = models.CharField(max_length=100, null=True)

    def __str__(self) -> str:
        return str(self.customer.name)+str(self.order_id)

    @property
    def get_order_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_order_quantity(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total



class OrderItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAdress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=500, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=100, null=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.address)

