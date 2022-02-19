from django.contrib import admin

from .models import Dish, Customer, CartItem, Cart, OrderItem, Order

admin.site.register([Dish, Customer, CartItem, Cart, Order, OrderItem])
