from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from store.models import *



class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username','email','password', 'password2')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()
        Customer.objects.create(
                user = user,
                name = user.first_name,
                email = user.email
            )

        return user

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class CartSerializers(serializers.ModelSerializer):
    customer = CustomerSerializers(many=False)
    cart_total = serializers.SerializerMethodField()
    cart_quantity = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = '__all__'

    def get_cart_total(self, obj):
        orderitems = obj.orderitem_set.all()
        cart_total = sum([item.get_total for item in orderitems])
        return cart_total
    
    def get_cart_quantity(self, obj):
        orderitems = obj.orderitem_set.all()
        cart_quantity = sum([item.quantity for item in orderitems])
        return cart_quantity


class OrderItemsSerializers(serializers.ModelSerializer):
    product = ProductSerializers(many=False)
    order = CartSerializers(many=False)
    total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = '__all__'


    def get_total(self, obj):
        total = obj.product.price * obj.quantity
        return total
    
class ProcessOrderSerializers(serializers.ModelSerializer):
    customer = CustomerSerializers(many=False)
    order = CartSerializers(many=False)
    class Meta:
        model = ShippingAdress
        fields = '__all__'