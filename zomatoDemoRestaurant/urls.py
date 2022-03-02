from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.homeView, name='zomatoDemoRestaurant'),
    path('menu/', views.menu, name='menu'),
    path('newdish/', views.newdish, name='newdish'),
    path('orders/', views.orders, name='resorders'),
]