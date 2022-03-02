from django.db import models
from zomatoDemoUsers.models import Users

# Create your models here.
class Restaurants(models.Model):
    username = models.OneToOneField(Users, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=100)
    restaurant_address = models.TextField()
    def __str__(self):
        return self.restaurant_name

class Dishes(models.Model):
    dish_name = models.CharField(max_length=100)
    dish_price = models.IntegerField()
    available_in = models.ManyToManyField(Users,related_name="restaurant_username")
    def __str__(self):
        return self.dish_name