import imp
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from .models import Dish, Customer, Cart, CartItem, Order, OrderItem
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Model


@login_required(login_url='/login')
def catalog(request):
    if request.method == 'POST':
        customer = Customer.objects.get(user=request.user)
        try:
            cart = Cart.objects.get(customer=customer)
            cartItems = CartItem.objects.filter(cart=cart)
        except:
            cart = Cart.objects.create(customer=customer)

        cartItems = CartItem.objects.filter(cart=cart)

        id = request.POST.get('dish-id')

        try:
            cartItem = cartItems.get(dish=Dish.objects.get(pk=id))
            cartItem.count += 1
            cartItem.save()
        except:
            CartItem.objects.create(
                dish=Dish.objects.get(pk=id), count=1, cart=cart
            )

    dishes = Dish.objects.all()

    return render(request, 'catalog/catalog.html', {'dishes': dishes})


@login_required(login_url='/login')
def addCartItem(request, pk, count):
    customer = Customer.objects.get(user=request.user)
    cart = Cart.objects.get(customer=customer)
    cartItems = CartItem.objects.filter(cart=cart)

    cartItem = cartItems.get(pk=pk)
    cartItem.count += 1
    cartItem.save()

    return redirect('/catalog/cart')


@login_required(login_url='/login')
def subtractCartItem(request, pk, count):
    customer = Customer.objects.get(user=request.user)
    cart = Cart.objects.get(customer=customer)
    cartItems = CartItem.objects.filter(cart=cart)

    cartItem = cartItems.get(pk=pk)
    if cartItem.count > 1:
        cartItem.count -= 1
        cartItem.save()
    else:
        cartItem.delete()

    return redirect('/catalog/cart')


@login_required(login_url='/login')
def cart(request):
    customer = Customer.objects.get(user=request.user)
    try:
        cart = Cart.objects.get(customer=customer)
        cartItems = CartItem.objects.filter(cart=cart)
    except:
        Cart.objects.create(customer=customer)
        cartItems = {}

    return render(request, 'catalog/cart.html', {'cartItems': cartItems})


@login_required(login_url='/login')
def makeOrder(request):
    customer = Customer.objects.get(user=request.user)
    cart = Cart.objects.get(customer=customer)

    cartItems = CartItem.objects.filter(cart=cart)
    if cartItems.count() >= 1:
        order = Order.objects.create(customer=customer)

        for item in cartItems:
            OrderItem.objects.create(dish=item.dish, count=item.count, order=order)

        cart.delete()
        Cart.objects.create(customer=customer)

    return redirect('/catalog')


def registration(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(
                user=user, name=user.username)
            return redirect('/login')

    return render(request, 'catalog/registration.html', {'form': form})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Login or password is wrong")

    return render(request, 'catalog/login.html')


def logoutPage(request):
    logout(request)

    return redirect('/login')
