from typing import OrderedDict
from django.forms import ModelForm
from django import forms
from catalog.models import Dish

class AddDishForm(ModelForm):
    class Meta:
        model = Dish
        fields = '__all__'


class EditDishForm(ModelForm):
    class Meta:
        model = Dish
        fields = '__all__'
