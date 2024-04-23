from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from main.models import Product, Supplier, Basket, CustomUser, Order
from main.permissions import IsOwnerOrReadOnly, IsOwner, IsOwnerSupplier, IsOwnerOrReadOnlyProduct, IsOwnerOrder, IsOwnerBasketBuyer
# test serializers
from main.serializers import CustomUserSerializer, SupplierSerializer, ProductSerializer, OrderSerializer, BasketSerializer

# working serializers
from main.serializers import CustomUserSerializer, SupplierViewSetSerializer, ProductModelViewSerializer, ProductGenericListSerializer, OrderSerializer, OrderGenericListSerializer, BasketModelViewetSerializer, BasketListForSupplierGenericListSerializer, CustomUserWorkSerializer
# WORKING VIEW

# CustomUser
class CustomUserWorkAPIVew(APIView):
    permission_classes = [IsAuthenticated, IsOwner] 

    # Получение своих данных пользователем
    def get(self, request):
        user_data = CustomUser.objects.filter(id= request.user.id)
        return Response({'User': CustomUserWorkSerializer(user_data, many=True).data})
    
    # изменение типа пользователя
    def post(self, request):
        if request.data['user_type'] not in ('BUYER', 'SUPPLIER'):
            raise ValueError('Тип пользователя должен соответствовать : BUYER / SUPPLIER')
        userdata = CustomUser.objects.filter(id= request.user.id).update(**request.data)
        return Response({'User': 'user data changed successfully'})

    # удаление аккаунта
    def delete(self, request):
        CustomUser.objects.filter(id= request.user.id).delete()
        return Response({'message': 'Ваш аккаунт был успешно удалён'})

# Supplier
class SupplierGenericCreateView(generics.CreateAPIView):
    '''Вью для поставщиков для работы с таблицей Supplier
    Поддерживает метод :
    - POST - для добавления поля. Создавать обьекты могут только Юзеры со статусом supplier (поставщики) '''
    serializer_class = SupplierViewSetSerializer
    permission_classes = [IsAuthenticated] 

        # передача поля supplier из токена
    def perform_create(self, serializer):
        serializer.save(supplier=self.request.user)

class SupplierGenericUpdateView(generics.UpdateAPIView):
    '''Вью для поставщиков-юзеров для работы с таблицей Supplier
    Поддерживает метод :
    - PATCH - для изменения поля activity'''
    def get_queryset(self):
        if self.request.user.user_type != 'SUPPLIER':
            raise ValueError('This path is only for SUPPLIER !!')
        return Supplier.objects.all()

    serializer_class = SupplierViewSetSerializer
    permission_classes = [IsAuthenticated, IsOwnerSupplier] 

# Product (for Supplier)
class ProductModelView(ModelViewSet):
    ''' вью для работы поставщиков с таблицей Product
    * Работает только от токена поставщика    '''
    queryset = Product.objects.all()
    serializer_class = ProductModelViewSerializer

    def get_queryset(self):
        '''данный метод срабатывает на GET/DELETE запросах'''
        if self.request.user.user_type != 'SUPPLIER':
            raise ValueError('This path is only for SUPPLIER !!')
        return Product.objects.all()

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyProduct] 

        # передача поля supplier из токена
    def perform_create(self, serializer):
        serializer.save(supplier=self.request.user)

# Product (for Buyer)
class ProductGenericListAPIView(generics.ListAPIView):
    '''Список товаров  из таблицы Product для Покупателя 
    * работает только от токена Покупателя
    - реализован только метод GET
    - показывает товары толь от поставщиков со статусом OPEN 
    - доступна фильтрация по поставщикам
    - доступна фильтрация по названию товара'''
    serializer_class = ProductGenericListSerializer
    # только для авторизованных пользователей
    permission_classes = [IsAuthenticated]
    # проверка на покупателя
    def get_queryset(self):
        if self.request.user.user_type != 'BUYER':
            raise ValueError('This path is only for BUYER !!')
        return Product.objects.filter(supplier__users__activity= 'OPEN')
    
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['supplier',]
    search_fields = ['name', ]

# Order 
class OrderModelView(ModelViewSet):
    '''вью для создания заказа
    * работает только от токена Покупателя
    - метод GET возвращает  текущий заказ со статусом  AWAITS
    - метод POST создает только один заказ со статусом AWAITS. Второй заказ со статусом AWAITS создать не возможно, пока статус заказа не будет изменен на ORDERED
    - метод PATCH доступен только для неоформленных заказов. Изменить заказ со статусом ORDERED уже невозможно    '''
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrder]

    # проверка на покупателя
    def get_queryset(self):
        if self.request.user.user_type != 'BUYER':
            raise ValueError('This path is only for BUYER !!')
        return Order.objects.filter(buyer= self.request.user, status= 'AWAITS')
 
    # передача поля buyer из токена
    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

 
# Basket (for Buyer)
class BasketModelView(ModelViewSet):
    '''вью для работы Покупателей с корзиной ( Basket )
    * работает только от токена Покупателя
    - метод POST добавляет товары в корзину автоматически проставляя id открытого заказа. Если открытого заказа несуществует, выдает ошибку'''
    queryset = Basket.objects.all()
    serializer_class = BasketModelViewetSerializer
    permission_classes = [IsAuthenticated, IsOwnerBasketBuyer]
    
    # проверка на покупателя
    def get_queryset(self):
        if self.request.user.user_type != 'BUYER':
            raise ValueError('This path is only for BUYER !!')
        res = Order.objects.filter(status= 'AWAITS', buyer= self.request.user)
        if len(res) == 0 :
            raise ValueError('ERROR !! У вас нет заказа Создайте пустой заказ') 
        return Basket.objects.filter(order= res[0].id)

    # передача поля order через токена
    def perform_create(self, serializer):
        res = Order.objects.filter(status= 'AWAITS', buyer= self.request.user)
        if len(res) == 0 :
            raise ValueError('ERROR !! У вас нет заказа Создайте пустой заказ')
        # print(' -8'*10)
        # print(res[0].id)
        serializer.save(order= res[0])


# Order (список продуктов в корзине)
class BasketListGenericListAPIView(generics.ListAPIView):
    '''список товаров добавленных в корзину покупателя
    * работает только от токена Покупателя
    - метод GET возвращает список товаров в корзине'''
    serializer_class = OrderGenericListSerializer
    permission_classes = [IsAuthenticated]

    # проверка на покупателя
    def get_queryset(self):
        if self.request.user.user_type != 'BUYER':
            raise ValueError('This path is only for BUYER !!')
        return Order.objects.filter(status= 'AWAITS', buyer= self.request.user)

# Order (список ранее оформленных заказов)
class OrderListGenericListAPIView(generics.ListAPIView):
    '''список оформленных заказов покупателя
    * работает только от токена Покупателя
    - метод GET возвращает список заказов со статусом ORDERED вместе с продуктами'''
    serializer_class = OrderGenericListSerializer
    permission_classes = [IsAuthenticated]
    # проверка на покупателя
    def get_queryset(self):
        if self.request.user.user_type != 'BUYER':
            raise ValueError('This path is only for BUYER !!')
        return Order.objects.filter(buyer= self.request.user, status= 'ORDERED')

# Basket (for SUPPLIER)(список заказанных товаров для поставщика )
class BasketListForSupplierGenericLAPIV(generics.ListAPIView):
    '''список заказанных товаров поставщика, добавленных в оформленные заказы Покупателей
    * работает только от токена Поставщика
    - метод GET возвращает список товаров из таблицы Basket у которых поле buyer__status == ORDERED'''
    serializer_class = BasketListForSupplierGenericListSerializer
    permission_classes = [IsAuthenticated]
    # проверка на покупателя
    def get_queryset(self):
        if self.request.user.user_type != 'SUPPLIER':
            raise ValueError('This path is only for SUPPLIER !!')
        return Basket.objects.filter(order__status= 'ORDERED', product__supplier = self.request.user)


































# TEST VIEWS
class CustomUserModelViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class =  CustomUserSerializer

class SupplierModelViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
 
class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderModelViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class BasketModelViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
