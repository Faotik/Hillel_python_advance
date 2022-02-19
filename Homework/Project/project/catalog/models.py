from statistics import mode
from telnetlib import STATUS
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=70)

    def __str__(self) -> str:
        return self.name


class Deliverer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=70)

    def __str__(self) -> str:
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name


class CartItem(models.Model):
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    count = models.IntegerField()
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.cart.customer.name}`s item - {self.dish.name}"


class Cart(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.customer.name}`s cart"


class Order(models.Model):
    STATUS = (
        ('In queue', 'In queue'),
        ('Cooking', 'Cooking'),
        ('Waiting deliverer', 'Waiting deliverer'),
        ('On delivery', 'On delivery'),
        ('Finished', 'Finished'),
    )

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS, default='In queue', blank=True)

    deliverer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.customer.name}`s order"


class OrderItem(models.Model):
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    count = models.IntegerField()
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.order.customer.name}`s order item - {self.dish.name}"
