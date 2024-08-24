from django.contrib import admin
from .models import *


@admin.register(AdminNotificationModel)
class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(UserNotificationModel)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ['title']
