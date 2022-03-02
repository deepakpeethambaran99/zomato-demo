from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from zomatoDemoAdmin.models import Restaurants, Dishes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.template.loader import render_to_string
from zomatoDemoCustomer.models import Cart, Orders
from .serializers import CartSerializer, DishSerializer
from django.db.models import Count, Sum
import datetime
from django.contrib import messages
# Create your views here
# @app_view(['GET'])
def menu(request,pk):
    restaurant = Restaurants.objects.get(id=pk)
    dishes = Dishes.objects.filter(available_in = restaurant.username)
    in_cart  = Cart.objects.filter(user = request.user,restaurant=restaurant)
    # serializerdish = DishSerializer(dishes,many=True)
    # serializercart = CartSerializer(cart_items,many = True)
    # data = {"data":serializerdish.data, "cart_items":serializercart.data}\
    context  = {"dishes" : dishes, "in_cart" : in_cart}
    if is_ajax(request):
            html    =   render_to_string('customer/menu.html',context,request=request)
            # print("render to string html : ",html)
            return JsonResponse({'menu':html})

def indexView(request):
    context = {}
    restaurants = Restaurants.objects.all()
    context['restaurants'] = restaurants
    items_in_cart = fetch_cart(request)
    context['items_in_cart'] = items_in_cart
    for item in items_in_cart:
        for dish in items_in_cart[item]:
            print(dish,dish.total_price)
    return render(request,"customer/index.html",context)

def dashboard(request):
    if request.user.is_superuser: 
        return redirect("/zomatoDemoAdmin")
    elif request.user.status == "restaurant": 
        return redirect("/zomatoDemoRestaurant")

def add_to_cart(request):
    
    context = {}
    if request.method == "GET":
        dish_id = request.GET['dish_id']
        restaurant_id = request.GET['res_id']
        already_in_cart = None
        try:
            already_in_cart = Cart.objects.get(dish = dish_id, restaurant = restaurant_id, order_placed = False)
        except:
            already_in_cart = None
            
        print("already in cart ",already_in_cart)
        
        if already_in_cart == None:
            restaurant_instance = Restaurants.objects.get(id=restaurant_id)
            user = request.user
            dish_instance = Dishes.objects.get(id=dish_id)

            #query to add item in cart
            add_to_cart = Cart(
                user = user,
                dish = dish_instance,
                restaurant = restaurant_instance,
                total_price = dish_instance.dish_price
            )
            add_to_cart.save()
            context['items_in_cart'] = fetch_cart(request)
            if is_ajax(request):
                html    =   render_to_string('customer/cart.html',context,request=request)
                # print("render to string html : ",html)
                return JsonResponse({'cart':html})

    else:
        return HttpResponse("Not working")

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


# filters the cart item by restaurants and returns the dictionary 
# {'restaurant_name' : '[items_in_cart]'}
def fetch_cart(request):
    restaurants_in_cart = Cart.objects.filter(user = request.user, order_placed = False).values('restaurant').annotate(count_restaurant = Count('restaurant'))
    items_per_restaurant = {}
    for restaurant in restaurants_in_cart:
        restaurant_instance = Restaurants.objects.get(id=restaurant['restaurant'])
        items_per_restaurant[restaurant_instance] = Cart.objects.filter(restaurant = restaurant_instance,user = request.user, order_placed = False)
    return items_per_restaurant

def update_quantity(request):
    context = {}
    if request.method == 'GET':
        id = request.GET['id']
        quantity = request.GET['quantity']
        dish = Cart.objects.get(id=id)
        dish.quantity = quantity
        dish.total_price = int(dish.quantity) * int(dish.dish.dish_price)
        dish.save() 
        return JsonResponse({'price': dish.total_price})

def remove_from_cart(request):
    context = {}
    if request.method == "GET":
        id = request.GET['id']
        dish = Cart.objects.get(id=id)
        dish.delete()
        context['items_in_cart'] = fetch_cart(request)
        if is_ajax(request):
            html    =   render_to_string('customer/cart.html',context,request=request)
            # print("render to string html : ",html)
            return JsonResponse({'cart':html})

def place_order(request,resid):

    #generate order id
    restaurant_instance = Restaurants.objects.get(id=resid)
    date = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S') )
    #format of order id #OID[user_id][datetime]
    order_id = "#OID" + str(request.user.id)  + date
    items = Cart.objects.filter(user=request.user, restaurant = restaurant_instance, order_placed = False)
    amount = 0
    for dish in items:
        amount += dish.total_price
    order_instance = Orders(
        order_id = order_id,
        user = request.user,
        restaurant = restaurant_instance,
        amount = amount,
    )
    order_instance.save()
    for item in items:
        order_instance.dishes.add(item)
    items.update(order_placed = True,order_id= order_id)
    messages.success(request,"Thank you! Your order has been placed successfully.")
    return redirect("/zomatoDemo/Home")

def prev_orders(request):
    context = {}
    orders = Orders.objects.filter(user = request.user)
    context['orders'] = orders
    return render(request,'customer/previousorder.html',context)