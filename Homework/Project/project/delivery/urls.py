from django.urls import path, include
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path('orders/waiting-deliverer/', views.toDeliverOrder),
    path('orders/active/', views.activeOrder),
    path('order/setOrderStatusToActive/<str:pk>/On delivery', views.setOrderStatusToActive),
    path('order/setOrderStatus/<str:pk>/Finished',
         views.setOrderStatusToFinished),
    path('', views.delivery),
]
