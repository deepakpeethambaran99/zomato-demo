from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users

class CustomUserCreationForm(UserCreationForm):
     class Meta:
         model = Users
         fields = "__all__"


class UserCreateForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Users
        fields =('username','email','password','confirm_password')
    
    def clean(self):
        cleaned_data = super(UserCreateForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm password does not match"
            )
    
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user