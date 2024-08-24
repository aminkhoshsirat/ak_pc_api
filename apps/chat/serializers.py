from rest_framework import serializers
from .models import *


class UserChatRoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserChatRoomModel
        fields = '__all__'


class UserChatSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserChatModel
        fields = '__all__'
