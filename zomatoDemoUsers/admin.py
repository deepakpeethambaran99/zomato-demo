from django.contrib import admin
from .models import  Users
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = Users
    add_form = CustomUserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Status',
            {
                "fields" : ( 'status',)
            }
        )
    )
    

admin.site.register(Users, CustomUserAdmin)