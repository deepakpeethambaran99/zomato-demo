from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('signin/authenticate', views.signin, name='authenticate'),
    path('login/authenticate', views.login, name='loginauthenticate'),
    path('logout/', views.logoutuser, name='logout'),
    path('registerrestaurant/', views.restaurantsView, name='register-restaurant'),
]