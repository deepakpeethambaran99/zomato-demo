from pyexpat import model
from rest_framework import serializers
from zomatoDemoAdmin.models import Dishes
from zomatoDemoCustomer.models import Cart

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'