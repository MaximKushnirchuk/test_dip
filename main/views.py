from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from main.models import Product, Supplier, Basket, CustomUser, Order
from main.permissions import IsOwnerOrReadOnly, IsOwner, IsOwnerSupplier

# test serializers
from main.serializers import CustomUserSerializer, SupplierSerializer, ProductSerializer, OrderSerializer, BasketSerializer

# working serializers
from main.serializers import SupplierViewSetSerializer

# WORKING VIEW

# Customuser
class CustomUserGenericUpdateView(generics.UpdateAPIView):
    '''вью для определения типа пользователя в таблице CustomUser 
    - работает только метод PATCH'''
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsOwner] 

# Supplier
class SupplierGenericCreateView(generics.CreateAPIView):
    '''Вью для поставщиков-юзеров для работы с таблицей Supplier
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
