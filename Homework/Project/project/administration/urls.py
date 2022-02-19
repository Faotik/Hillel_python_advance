from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.administration),
    path('catalog/', views.catalog),
    path('catalog/add-dish/', views.createDish),
    path('catalog/edit-dish/<str:pk>', views.editDish),
    path('catalog/delete-dish/<str:pk>', views.deleteDish),
    path('orders/queue/', views.queue),
    path('orders/cooking/', views.cookingOrder),
    path('order/setOrderStatus/<str:pk>/<str:status>', views.setOrderStatus)
]
