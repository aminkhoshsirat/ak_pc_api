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
    fullname = serializers.CharField(max_length=1000)
    password = serializers.CharField(max_length=25)
    confirm_password = serializers.CharField(max_length=25)

    def validate(self, data):
        confirm_password = data['confirm_password']
        password = data['password']

        if confirm_password == password:
            if password.isdigit() or password.isalpha() or password.lower() == password or len(password) < 8:
                raise serializers.ValidationError('پسورد باید شامل اعداد و حروف کوچک و بزرگ باشد')
            else:
                return data
        else:
            raise serializers.ValidationError('پسورد و تکرار آن یکی نمی باشد')


class ActivationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    phone = serializers.CharField(max_length=11)
    email = serializers.EmailField()
    fullname = serializers.CharField(max_length=1000)
    password = serializers.CharField(max_length=25)
    confirm_password = serializers.CharField(max_length=25)

    def validate(self, data):
        confirm_password = data['confirm_password']
        password = data['password']

        if confirm_password == password:
            if password.isdigit() or password.isalpha() or password.lower() == password or len(password) < 8:
                raise serializers.ValidationError('پسورد باید شامل اعداد و حروف کوچک و بزرگ باشد')
            else:
                return data
        else:
            raise serializers.ValidationError('پسورد و تکرار آن یکی نمی باشد')


class UserAddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserAddressModel
        fields = '__all__'


class SendOtpSerializers(serializers.Serializer):
    phone = serializers.CharField(max_length=11)

