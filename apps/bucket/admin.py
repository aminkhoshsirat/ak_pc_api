from django.contrib import admin
from .models import *


@admin.register(BuketModel)
class BucketAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_paid']


@admin.register(BucketProductsModel)
class BucketAdmin(admin.ModelAdmin):
    list_display = ['bucket']