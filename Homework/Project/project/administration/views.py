from django.shortcuts import redirect, render

from catalog.models import Dish, Order, OrderItem
from .forms import AddDishForm, EditDishForm
from django.contrib.auth.decorators import user_passes_test, login_required


def is_administration(user):
    return user.groups.filter(name='Administrator').exists()


@login_required(login_url='/login')
@user_passes_test(is_administration, login_url='/login')
def administration(request):
    return render(request, 'administration/administration.html')


@login_required(login_url='/login')
@user_passes_test(is_administration, login_url='/login')
def catalog(request):
    dishes = Dish.objects.all()
    return render(request, 'administration/catalog.html', {'dishes': dishes})


@login_required(login_url='/login')
@ user_passes_test(is_administration, login_url='/login')
def createDish(request):
    form = AddDishForm

    if request.method == 'POST':
        form = AddDishForm(request.POST)
        if(form.is_valid):
            form.save()
            return redirect('/administration/catalog')

    context = {'form': form}
    return render(request, 'administration/add-dish.html', context)


@login_required(login_url='/login')
@ user_passes_test(is_administration, login_url='/login')
def editDish(request, pk):
    dish = Dish.objects.get(id=pk)

    form = EditDishForm(instance=dish)

    if request.method == 'POST':
        form = EditDishForm(request.POST, instance=dish)
        if(form.is_valid):
            form.save()
            return redirect('/administration/catalog')

    context = {'form': form, 'dish': dish}
    return render(request, 'administration/edit-dish.html', context)


@login_required(login_url='/login')
@ user_passes_test(is_administration, login_url='/login')
def deleteDish(request, pk):
    dish = Dish.objects.get(id=pk)

    dish.delete()

    return redirect('/administration/catalog')


@login_required(login_url='/login')
@ user_passes_test(is_administration, login_url='/login')
def queue(request):
    order = Order.objects.filter(status='In queue')
    orderItemsList = list()
    for o in order:
        orderItems = OrderItem.objects.filter(order=o)
        orderItemsList.append(orderItems)
    return render(request, 'administration/order-queue.html', {'order': order, 'orderItemsList': orderItemsList})


@login_required(login_url='/login')
@ user_passes_test(is_administration, login_url='/login')
def setOrderStatus(request, pk, status):
    order = Order.objects.get(pk=pk)
    order.status = status
    order.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/login')
@ user_passes_test(is_administration, login_url='/login')
def cookingOrder(request):
    order = Order.objects.filter(status='Cooking')
    orderItemsList = list()
    for o in order:
        orderItems = OrderItem.objects.filter(order=o)
        orderItemsList.append(orderItems)
    return render(request, 'administration/order-cooking.html', {'order': order, 'orderItemsList': orderItemsList})
