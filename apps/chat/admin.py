from django.contrib import admin
from .models import *


@admin.register(UserChatRoomModel)
class UserChatRoomAdmin(admin.ModelAdmin):
    list_display = ['user']



@admin.register(UserChatModel)
class UserChatAdmin(admin.ModelAdmin):
    list_display = ['text', 'date']