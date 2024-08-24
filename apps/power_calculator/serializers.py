from rest_framework import serializers
from .models import *


class GpuBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GpuBrandsModel
        fields = '__all__'


class GpuSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GpuSeriesModel
        fields = '__all__'


class GpuSerializer(serializers.ModelSerializer):
    class Meta:
        model = GpuModel
        fields = '__all__'


class MainBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainBoardModel
        fields = '__all__'


class SSDSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSDModel
        fields = '__all__'


class HardSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardModel
        fields = '__all__'


class RamSerializer(serializers.ModelSerializer):
    class Meta:
        model = RamModel
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriveModel
        fields = '__all__'


class FanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FanModel
        fields = '__all__'


class LiquidSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiquidFanModel
        fields = '__all__'
