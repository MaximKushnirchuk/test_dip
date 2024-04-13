from django.db import models

from django.contrib.auth.models import AbstractUser

class SupplierStatusChoices(models.TextChoices):
    """Статусы поставщика"""
    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"

class OrderStatusChoices(models.TextChoices):
    """Статусы заказа"""
    AWAITS = 'AWAITS', 'Ожидает'
    ORDERED = 'ORDERED', 'Заказано'
    SENT = 'SENT', 'Отправлено'

class UserTypeChoices(models.TextChoices):
    """Статусы поставщика"""
    BUYER = "BUYER", "Покупатель"
    SUPPLIER = "SUPPLIER", "Поставщик"

###### MODELS ############
class CustomUser(AbstractUser):
    user_type = models.TextField(choices= UserTypeChoices.choices)

    # def __str__(self) -> str:
    #     return self.username

    def Meta():
        db_table = 'User'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Supplier(models.Model):
    supplier = models.OneToOneField(CustomUser, on_delete= models.CASCADE, related_name= 'users')
    activity = models.TextField(choices= SupplierStatusChoices.choices,
                                default= SupplierStatusChoices.OPEN)

    # def __str__(self) -> str:
    #     return self.supplier

    def Meta():
        db_table = 'Supplier'
        ordering = ['activity']
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits= 10, decimal_places= 2)
    balance = models.PositiveIntegerField()
    supplier = models.ForeignKey(CustomUser, on_delete= models.CASCADE,
                                  related_name= 'products')
    
    # def __str__(self) -> str:
    #     return self.name

    def Meta():
        db_table = 'Product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class Order(models.Model):
    buyer = models.ForeignKey(CustomUser, on_delete= models.CASCADE, related_name= 'orders')
    adress = models.CharField(max_length=150)
    status = models.TextField(choices= OrderStatusChoices.choices,
                                    default = OrderStatusChoices.AWAITS)
    # def __str__(self) -> str:
    #     return self.buyer

    def Meta():
        db_table = 'Order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class Basket(models.Model):
    order = models.ForeignKey(Order, on_delete= models.CASCADE,
                              related_name= 'inbasket')
    product = models.ForeignKey(Product, on_delete= models.CASCADE,
                              related_name= 'productinbasket')
    quantity = models.PositiveSmallIntegerField(default= 1)

    # def __str__(self) -> str:
    #     return self.quanity


 