from pprint import pprint

from rest_framework import serializers
from main.models import CustomUser, Product, Basket, Supplier, Order


#  WORKING SERIALIZERS

#  сериалайзер для CustomUserWorkAPIVew метода GET
class CustomUserWorkSerializer(serializers.Serializer):
    '''сериалайзер для отображения данных своего аккаунта'''
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    user_type = serializers.CharField()

# сериалайзер для таблицы Supplier
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

# сериалайзер для таблицы Product (для поставщиков)
class ProductModelViewSerializer(serializers.ModelSerializer):
    '''ограничения :
    - минимально возможная длина названия товара 2 символа
    - минимально возможная длина описания товара 10 символов
    - минимально возможная цена 0,01'''
    name = serializers.CharField(min_length=2)
    description = serializers.CharField(min_length=10)
    price = serializers.DecimalField(max_digits= 10, decimal_places= 2, min_value= 0.01)
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'balance', 'supplier')
        read_only_fields = ('supplier',)

    # проверка токена - только для поставщика
    def create(self, validated_data):
        if validated_data['supplier'].user_type != 'SUPPLIER':
            raise ValueError(' * * * TYPE USER  ERROR.  This method is only for supplier !!')
        return Product.objects.create(**validated_data)

# сериалайзер для таблицы Product (для покупателей)
class ProductGenericListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits= 10, decimal_places= 2)
    balance = serializers.IntegerField()
    supplier = serializers.CharField()

# сериалайзер для таблицы Order (общий для тестов и рабочий)
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'buyer', 'adress', 'status')
        read_only_fields = ('buyer',)

    def create(self, validated_data):
        # проверка токена - только для Покупателя
        if validated_data['buyer'].user_type != 'BUYER':
            raise ValueError(' * * * TYPE USER  ERROR.  This method is only for BUYER !!')
        # проверка единственного открытого заказа
        order_awaits = Order.objects.filter(buyer= validated_data['buyer'], status= 'AWAITS')
        if len(order_awaits) != 0:
            raise ValueError('ERROR !! У Вас уже есть открытый заказ. Оформите его либо удалите, прежде чем создавать новый')

        return Order.objects.create(**validated_data)

# сериалайзер для получения покупателем списка своиз заказов 
class InnerProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.CharField()
    supplier = serializers.CharField()
class InnerBasketSerializer(serializers.Serializer):
    product = InnerProductSerializer()
    quantity = serializers.IntegerField()
class OrderGenericListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    adress = serializers.CharField()
    status = serializers.CharField()
    inbasket = InnerBasketSerializer(many= True)

# сериалайзер для работы покупателей с корзиной (Basket)
class BasketModelViewetSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value= 1, default= 1)
    '''сериалайзер обеспечивает работу Покупателя с таблицей Basket
    - добавлять товар в коорзину может только Покупатель 
    - товар добавляется в корзину только от Поставщиков со статусом OPEN
    - минимальное количеситво товара для добавления = 1
    - если не указать количество товара, по умолчанию добавляется одеа еденица
    - если количество товара в заказе превышает отстатки на складе - выводится ошибка
    - при добавлении товара который уже есть в корзине - прибавляется его количество и выводится сообщение что такой товар уже добавлен
    - при добавлении товара в корзину автоматически изменяются его остатки на складе
    '''
    class Meta:
        model = Basket
        fields = ('id', 'product', 'quantity', 'order')
        read_only_fields = ('order',)

    def create(self, validated_data):
        
        # проверка  покупателя
        if validated_data['order'].buyer.user_type != 'BUYER':
            raise ValueError('TYPE USER  ERROR !!!! Добавлять товары в корзину может только покупатель')

        #  проверка статуса поставщика
        if validated_data['product'].supplier.users.activity != 'OPEN':
            raise ValueError('USER ACTIVITY ERROR !!!! Supplier CLOSED  -  DONT WORK ')

        # проверка количества товара на складе 
        product_balance = validated_data['product'].balance
        product_quantity = validated_data['quantity']
        if  product_quantity > product_balance :
            raise ValueError('QUANTITY  ERROR  !!!!  Balance product is too small !!!')

        # Изменение остатков товара (Product.balance)  на складе
        Product.objects.filter(id= validated_data['product'].id).update(balance= product_balance - product_quantity)

        # проверка повторности товара: либо добавляем товар в корзину, либо увеличиваем количество
        basket_list = Basket.objects.filter(order= validated_data['order'])
        for one_product in basket_list:
            if validated_data['product'] ==  one_product.product :
                Basket.objects.filter(id= one_product.id).update(quantity= validated_data['quantity'] + one_product.quantity)
                raise ValueError('ERROR  PRODUCT  COUNT!!  Этот товар уже есть в корзине. Добавлено количество ')


        return Basket.objects.create(**validated_data)

# сериалайзер для списка продуктов в корзине
class InnerForOrderAdressSerializer(serializers.Serializer):
    buyer = serializers.CharField()
    adress = serializers.CharField()
class BasketListForSupplierGenericListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product = InnerProductSerializer()
    quantity = serializers.IntegerField()
    order = InnerForOrderAdressSerializer()



















# TEST serializers
class CustomUserSerializer(serializers.ModelSerializer):
    '''используется для ТЕСТОВЫХ ЗАПРОСОВ'''
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'user_type')

class SupplierSerializer(serializers.ModelSerializer):
    supplier = CustomUserSerializer()
    class Meta:
        model = Supplier
        fields = ('id', 'activity', 'supplier')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class TestOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = '__all__'

        
   