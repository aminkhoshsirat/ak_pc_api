from rest_framework import serializers
from .models import *


class AsembleSerializers(serializers.ModelSerializer):
    asemble_products = serializers.StringRelatedField(many=True)

    class Meta:
        model = AsembleModel
        fields = '__all__'


class AsembleProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = AsembleProductsModel
        fields = '__all__'
