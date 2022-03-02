from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here.


class Users(AbstractUser):
    restaurant = "restaurant"
    customer = "customer"
    status_choices = [(restaurant,'restaurant'),(customer,'customer'),]
    status = models.CharField(max_length=50,choices=status_choices,default=restaurant)