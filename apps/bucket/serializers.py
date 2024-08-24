from rest_framework import serializers
from .models import *


class BucketSerializers(serializers.ModelSerializer):

    class Meta:
        model = BuketModel
        fields = '__all__'


class BucketProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = BucketProductsModel
        fields = '__all__'


class WalletSerializers(serializers.ModelSerializer):
    class Meta:
        model = WalletModel
        fields = '__all__'


class WalletTransactionSerializers(serializers.ModelSerializer):
    class Meta:
        model = WalletTransactionModel
        fields = '__all__'
