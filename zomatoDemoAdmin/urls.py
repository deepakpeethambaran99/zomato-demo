from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.indexView, name='zomatoDemoAdmin'),
    path('restaurants/', views.restaurantsView, name='restaurants'),
    path('dishes/', views.dishesView, name='dishes'),
]