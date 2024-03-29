from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.filters import SearchFilter

from main.models import Product, Supplier, Basket, CustomUser, Order

class ProductViewSet(viewsets.ViewSet):
    pass
    # список товаров только от поставщиков со статусом OPEN
    # def list(self, request):
    #     queryset = Product.objects.filter(supplier__users__activity = 'OPEN')
    #     serializer = ProductSerializer(queryset, many=True)
    #     # filter_backends = [SearchFilter]
    #     # search_fields = ['name',]
    #     return Response(serializer.data)
    
    # def create(self, request):
    #     queryset = Product.objects.create()
    #     serializer = ProductSerializer(queryset)
    #     return Response(serializer.data)


    # def destroy(self, request):
    #     pass






# TEST VIEWS
from main.serializers import CustomUserSerializer, SupplierSerializer, ProductSerializer, OrderSerializer, BasketSerializer
class CustomUserModelViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

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
