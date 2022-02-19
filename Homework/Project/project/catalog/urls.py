from django.urls import path, include
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path('', lambda request: redirect('/catalog/')),
    path('catalog/add-cart-item/<str:pk>/<str:count>', views.addCartItem),
    path('catalog/subtract-cart-item/<str:pk>/<str:count>', views.subtractCartItem),
    path('catalog/', views.catalog),
    path('catalog/cart/', views.cart),
    path('catalog/make-order/', views.makeOrder),
    path('registration/', views.registration),
    path('login/', views.loginPage),
    path('logout/', views.logoutPage),
]
