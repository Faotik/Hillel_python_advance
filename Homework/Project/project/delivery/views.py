from django.shortcuts import render, redirect
from catalog.models import Dish, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test, login_required


def is_deliverer(user):
    return user.groups.filter(name='Deliverer').exists()


@login_required(login_url='/login')
@user_passes_test(is_deliverer, login_url='/login')
def toDeliverOrder(request):
    order = Order.objects.filter(status='Waiting deliverer')
    orderItemsList = list()
    for o in order:
        orderItems = OrderItem.objects.filter(order=o)
        orderItemsList.append(orderItems)
    return render(request, 'delivery/order-waiting-delivery.html', {'order': order, 'orderItemsList': orderItemsList})


@login_required(login_url='/login')
@user_passes_test(is_deliverer, login_url='/login')
def setOrderStatusToActive(request, pk):
    status = 'On delivery'
    order = Order.objects.get(pk=pk)
    order.status = status
    order.deliverer = request.user
    order.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/login')
@user_passes_test(is_deliverer, login_url='/login')
def setOrderStatusToFinished(request, pk):
    status = 'Finished'
    try:
        order = Order.objects.get(pk=pk, deliverer=request.user)
        order.status = status
        order.save()

        return redirect(request.META.get('HTTP_REFERER', '/'))
    except:
        return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/login')
@user_passes_test(is_deliverer, login_url='/login')
def activeOrder(request):
    order = Order.objects.filter(status='On delivery', deliverer=request.user)
    orderItemsList = list()
    for o in order:
        orderItems = OrderItem.objects.filter(order=o)
        orderItemsList.append(orderItems)
    return render(request, 'delivery/order-active.html', {'order': order, 'orderItemsList': orderItemsList})


@login_required(login_url='/login')
@user_passes_test(is_deliverer, login_url='/login')
def delivery(request):
    return render(request, 'delivery/delivery.html')
