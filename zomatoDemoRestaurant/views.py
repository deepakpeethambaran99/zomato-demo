from pdb import Restart
from queue import Empty
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from zomatoDemoAdmin.models import Dishes, Restaurants
from zomatoDemoAdmin.forms import DishesForm
from django.contrib import messages
import validators
from zomatoDemoCustomer.models import Orders,Cart
from django.db.models import Count
import datetime
import dateutil.relativedelta
# Create your views here.
@login_required(login_url='/zomatoDemo/login/')
@user_passes_test(lambda u: u.status == "restaurant")
def homeView(request):
    context = {}
    
    to_date = datetime.datetime.today()
    from_date = to_date - dateutil.relativedelta.relativedelta(months=1)
    
    if request.method == "POST":
        from_date = request.POST.get('fromDate')
        to_date = request.POST.get('toDate')
        


    restaurant_instance = Restaurants.objects.get(username = request.user)
    sales_of_dish_by_date = Orders.objects.filter(order_date__range=[from_date, to_date],restaurant = restaurant_instance)
    sales_data = sales_of_dish_by_date.values('dishes').annotate(dishes_count = Count('dishes'))

    for s in sales_data:
        cart_item = Cart.objects.get(id=s['dishes'])
        s['dish_details'] = cart_item
        s['dishes_count'] = cart_item.quantity * s['dishes_count']
        

    context['todate'] = to_date
    context['fromdate'] = from_date
    context['sales_data'] = sales_data
    return render(request,"restaurant/home.html",context)


@login_required(login_url='/zomatoDemo/login/')
@user_passes_test(lambda u: u.status == "restaurant")
def menu(request):
    context = {}
    dishes = Dishes.objects.all()
    context["dishsuggestion"] = dishes

    dishes_form = DishesForm()
    context["dishes_form"] = dishes_form
    
    dish_available = Dishes.objects.filter(available_in = request.user).order_by("dish_name")
    context["dishes"] = dish_available
    if request.method == "POST":
        dishname = request.POST['dishname']
        if validators.is_empty(dishname):
            return render(request,"restaurant/menu.html",context)
        dishname,price = dishname.split(' -Rs. ')
        print("dishname",dishname)
        dish = Dishes.objects.get(dish_name=dishname,dish_price=price)
        dish.available_in.add(request.user)
        messages.success(request,"Dish Added to your menu.")
    return render(request,"restaurant/menu.html",context)

@login_required(login_url='/zomatoDemo/login/')
@user_passes_test(lambda u: u.status == "restaurant")
def newdish(request):
    context = {}
    dishes = Dishes.objects.all()
    context["dishsuggestion"] = dishes

    dish_available = Dishes.objects.filter(available_in = request.user).order_by("dish_name")
    context["dishes"] = dish_available
    if request.method == "POST":
        dishname = request.POST['dish_name']
        dishprice = request.POST['dish_price']
        try:
            is_dish_available = Dishes.objects.get(dish_name=dishname,dish_price=dishprice)
            #print("available",is_dish_available.dish_name)
        except:
            is_dish_available = None
        
        print("is_dish",is_dish_available)
        if is_dish_available != None:
            messages.error(request,"Dish already exists with this price. Try with different price.")
            dishes_form = DishesForm()
            context["dishes_form"] = dishes_form
            return redirect('/zomatoDemoRestaurant/menu')
        else:
            dishes_form = DishesForm(request.POST)

            if dishes_form.is_valid():
                dishes_form.save()
                dishes_form = DishesForm()
                context["dishes_form"] = dishes_form
                messages.success(request,"Dish Added now you can add it to your menu.")
            else:
                context["dishes_form"] = dishes_form
            
            return redirect('/zomatoDemoRestaurant/menu')
    else:
        return redirect('/zomatoDemoRestaurant/menu')


def orders(request):
    context = {}
    restuarant = Restaurants.objects.get(username = request.user)
    orders = Orders.objects.filter(restaurant= restuarant)
    context['orders'] = orders
    return render(request,"restaurant/orders.html",context)