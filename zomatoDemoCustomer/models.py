from django.db import models
from zomatoDemoAdmin.models import Dishes, Restaurants
from zomatoDemoUsers.models import Users

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    order_id = models.ForeignKey('Orders',max_length=100,null=True, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurants,on_delete=models.CASCADE)
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(default= 1)
    order_placed = models.BooleanField(default = False) 

    def __str__(self):
        return self.dish.dish_name

class Orders(models.Model):
    order_id = models.CharField(primary_key=True, max_length = 100 )
    restaurant = models.ForeignKey(Restaurants,on_delete=models.CASCADE)
    dishes = models.ManyToManyField(Cart )
    user =models.ForeignKey(Users,on_delete=models.CASCADE)
    amount = models.IntegerField()
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id
