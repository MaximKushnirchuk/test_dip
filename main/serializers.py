from rest_framework import serializers
from main.models import CustomUser, Product, Basket, Supplier, Order

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'    

class ProductSerializer(serializers.ModelSerializer):
    # supplier = CustomUserSerializer(read_only= True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'balance', 'supplier')

    def create(self, validated_data):
        # print(validated_data)
        return Product.objects.create(**validated_data)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class Helper(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('buyer',)
class BasketSerializer(serializers.ModelSerializer):
    order = Helper()
    class Meta:
        model = Basket
        fields = ('id', 'order', 'product', 'quantity')
        # read_only_fields = ('order',)