from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import DishesForm, RestaurantsForm
from .models import Dishes, Restaurants
from zomatoDemoUsers.models import Users
from zomatoDemoUsers.forms import UserCreateForm
from django.contrib import messages

@login_required(login_url='/zomatoDemo/login/')
@user_passes_test(lambda u: u.is_superuser)
def indexView(request):
    return render(request,"zomatoDemoAdmin/home.html")

@login_required(login_url='/zomatoDemo/login/')
@user_passes_test(lambda u: u.is_superuser)
def restaurantsView(request):
    context = {}
    
    restaurant = Restaurants.objects.all().order_by('restaurant_name')
    
    #print(restaurant)
    if request.method == "POST":
        user_form = UserCreateForm(request.POST)
        restaurant_form = RestaurantsForm(request.POST)
        if user_form.is_valid() and restaurant_form.is_valid():
            u = user_form.save()
            r = restaurant_form.save(commit = False)
            r.username = u
            r.save()
            user_form = UserCreateForm()
            restaurant_form = RestaurantsForm()
            messages.success(request,"Restaurant Added.")
            context = {"userform":user_form, "restaurantform":restaurant_form , "restaurants":restaurant}
        else:
            context = {"userform":user_form, "restaurantform":restaurant_form , "restaurants":restaurant}
    else:
        user_form = UserCreateForm()
        restaurant_form = RestaurantsForm()
        context = {"userform":user_form, "restaurantform":restaurant_form,"restaurants":restaurant }
    return render(request,"zomatoDemoAdmin/restaurants.html",context)

@login_required(login_url='/zomatoDemo/login/')
@user_passes_test(lambda u: u.is_superuser)
def dishesView(request):
    context = {}
    dishes = Dishes.objects.all().order_by('dish_name')
    
    context["dishes"] = dishes
    if request.method == "POST":
        dishname = request.POST['dish_name']
        dishprice = request.POST['dish_price']
        try:
            is_dish_available = Dishes.objects.get(dish_name=dishname,dish_price=dishprice)
            messages.error(request,"Dish already exists with this price. Try with different price.")
            dishes_form = DishesForm()
            context["dishes_form"] = dishes_form
            return render(request,"zomatoDemoAdmin/dishes.html",context)
        except:
            dishes_form = DishesForm(request.POST)

            if dishes_form.is_valid():
                dishes_form.save()
                dishes_form = DishesForm()
                context["dishes_form"] = dishes_form
                messages.success(request,"Dish Added.")
            else:
                context["dishes_form"] = dishes_form

    else:
        dishes_form = DishesForm()
        context["dishes_form"] = dishes_form
    return render(request,"zomatoDemoAdmin/dishes.html",context)