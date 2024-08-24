from rest_framework import serializers
from .models import *


class AdminNotificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = AdminNotificationModel
        fields = '__all__'


class UserNotificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserNotificationModel
        fields = '__all__'
