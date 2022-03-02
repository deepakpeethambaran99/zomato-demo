from django.contrib import admin
from .models import Dishes, Restaurants
from zomatoDemoUsers.models import Users
# Register your models here.
class DishesAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "available_in":
            kwargs["queryset"] = Users.objects.filter(status='restaurant')
        return super(DishesAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(Dishes, DishesAdmin)
admin.site.register(Restaurants)