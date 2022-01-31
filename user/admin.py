from django.contrib import admin
from .models import CustomUserModel
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model=CustomUserModel


admin.site.register(CustomUserModel, CustomUserAdmin)

# Register your models here.
