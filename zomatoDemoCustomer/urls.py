from django.contrib import admin
from django.urls import path, include


from . import views
urlpatterns = [
    path('', views.indexView, name='zomatoDemoHome'),
    path('dashboard/', views.dashboard, name='gotodashboard'),
    path('menulist/<int:pk>', views.menu, name='menu-list'),

    path('cart/quantity/', views.update_quantity, name='quantity'),
    path('cart/remove/', views.remove_from_cart, name='remove-from-cart'),
    path('cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/place-order/<int:resid>', views.place_order, name='place-order'),
    path('orders/', views.prev_orders, name='orders'),
]