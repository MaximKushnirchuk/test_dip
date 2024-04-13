from pprint import pprint

from rest_framework import serializers
from main.models import CustomUser, Product, Basket, Supplier, Order


#  WORKING SERIALIZERS

# сериалайзер для таблицы CustomUser
class CustomUserSerializer(serializers.ModelSerializer):
    '''используется для CustomUserGenericCreateView'''
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'user_type')

class SupplierViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('id', 'supplier', 'activity')
        read_only_fields = ('supplier',)

    # проверка статуса поставщика
    def create(self, validated_data):
        if validated_data['supplier'].user_type != 'SUPPLIER':
            raise ValueError('TYPE USER  ERROR !!!! This IS ONLY FOR SUPPLIER')
        return Supplier.objects.create(**validated_data)


























# TEST serializers


class SupplierSerializer(serializers.ModelSerializer):
    supplier = CustomUserSerializer()
    class Meta:
        model = Supplier
        fields = ('id', 'activity', 'supplier')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = '__all__'

        
   