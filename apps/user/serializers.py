from rest_framework import serializers
from .models import *


class UserSerializers(serializers.Serializer):
    class Meta:
        model = UserModel
        fields = '__all__'


class LoginSerializers(serializers.Serializer):
    phone_or_email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=25)


class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=25)
    confirm_password = serializers.CharField(max_length=25)

    def validate_confirm_password(self):
        confirm_password = self.data['confirm_password']
        password = self.data['password']

        if confirm_password == password:
            if password.isdigit() or password.isalpha() or password.lower() == password:
                raise serializers.ValidationError('پسورد باید شامل اعداد و حروف کوچک و بزرگ باشد')
            else:
                return confirm_password
        else:
            raise serializers.ValidationError('پسورد و تکرار آن یکی نمی باشد')


class UserAddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserAddressModel
        fields = '__all__'

