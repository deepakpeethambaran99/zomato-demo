from email import message
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Users
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login,logout
from zomatoDemoAdmin.models import Restaurants
import validators as validate
from .forms import UserCreateForm
from zomatoDemoAdmin.forms import RestaurantsForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def loginView(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/zomatoDemoAdmin')
        if request.user.status == "restaurant":
            return redirect('/zomatoDemoRestaurant')
        else:
            return redirect('/zomatoDemo/Home')
    else:
        return render(request,"userAuth/login.html")



def signin(request):
    if request.method == "POST":
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        email_id = request.POST["emailid"]
        username = request.POST["username"]
        password = request.POST["password"]
        confirmpassword = request.POST["confirmpassword"]
        error = False
        #print(first_name,last_name,email_id,username,password,confirmpassword)
        if password is confirmpassword:
            messages.error(request, "Password does not matched. Please re-enter password")
            error = True
        if not validate.validateName(first_name) and not validate.validateName(last_name): 
            messages.error(request, "Please enter valid first and last name.")
            error = True
        
        try: 
            email_present = Users.objects.get(email = email_id)
        except:
            email_present = None
        if email_present is not None:
            messages.error(request,"User is already exist with this email id please try to login.")
            return redirect("signin")
        if error:
            return redirect("signin")
            
        else:
            try:
                username_present = Users.objects.get(username = username)
            except:
                username_present = None

            if username_present is not None:
                messages.error(request,"Username already exists")
                return redirect("signin")
            else:
                user = Users.objects.create_user(first_name = first_name,last_name=last_name,email=email_id,username=username,password=password,is_staff=False,status="customer")
                messages.success(request, "You are successfully registered. Need login.")
                user.save()
                return redirect('login')
    else:
        return render(request,"userAuth/signup.html")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
    if user is not None:
        dj_login(request,user)
        if user.is_superuser:
            return redirect('/zomatoDemoAdmin')
        if user.status == "restaurant":
            return redirect('/zomatoDemoRestaurant')
        else:
            return redirect('/zomatoDemo/Home')
    else:
        messages.error(request, "Invalid user credentials")
        return redirect('login')

def logoutuser(request):
    logout(request)
    return redirect('/zomatoDemo/login/')

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
            return redirect('login')
        else:
            context = {"userform":user_form, "restaurantform":restaurant_form , "restaurants":restaurant}
    else:
        user_form = UserCreateForm()
        restaurant_form = RestaurantsForm()
        context = {"userform":user_form, "restaurantform":restaurant_form,"restaurants":restaurant }
    return render(request,"userAuth/registerrestaurant.html",context)
