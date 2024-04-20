"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rest_framework.routers import DefaultRouter

# test view
from main.views import CustomUserModelViewSet, SupplierModelViewSet, ProductModelViewSet, OrderModelViewSet, BasketModelViewSet

# WORKING VIEWS
from main.views import CustomUserGenericUpdateView, SupplierGenericUpdateView, SupplierGenericCreateView, ProductModelView, ProductGenericListAPIView, OrderModelView, OrderListGenericListAPIView, BasketModelView, BasketListGenericListAPIView, BasketListForSupplierGenericLAPIV

r = DefaultRouter()
# test_view_routs
r.register('users', CustomUserModelViewSet)
r.register('suppliers', SupplierModelViewSet)

# working routs
r.register('product', ProductModelView)
r.register('order', OrderModelView)
r.register('basket', BasketModelView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customuser/<int:pk>/', CustomUserGenericUpdateView.as_view()),
    path('supplier/', SupplierGenericCreateView.as_view()),
    path('activity/<int:pk>/', SupplierGenericUpdateView.as_view()),
    path('productlist/', ProductGenericListAPIView.as_view()),
    path('orderlist/', OrderListGenericListAPIView.as_view()),
    path('basketlist/', BasketListGenericListAPIView.as_view()),
    path('basketlistsupplier/', BasketListForSupplierGenericLAPIV.as_view()),

] + r.urls


