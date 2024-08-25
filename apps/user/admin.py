from django.contrib import admin
from .models import *


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone', 'ban', 'profile_image', 'register_date', 'post_code']


@admin.register(UserAddressModel)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['state']