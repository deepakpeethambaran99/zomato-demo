from django import forms
from .models import Dishes, Restaurants

class RestaurantsForm(forms.ModelForm):
    class Meta:
        model = Restaurants
        fields = ["restaurant_name","restaurant_address"]

class DishesForm(forms.ModelForm):
    class Meta:
        model = Dishes
        fields = ("dish_name","dish_price")