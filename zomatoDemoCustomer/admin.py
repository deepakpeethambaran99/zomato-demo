from django.contrib import admin

from zomatoDemoCustomer.models import Cart, Orders

# Register your models here.
admin.site.register(Cart)
admin.site.register(Orders)