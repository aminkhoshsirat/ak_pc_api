from rest_framework import serializers
from .models import *


class SiteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteDetailModel
        fields = '__all__'


class AdvertisingBannerSerializers(serializers.ModelSerializer):
    class Meta:
        model = AdvertisingBannerModel
        fields = '__all__'


class InstantOfferSerializers(serializers.ModelSerializer):
    class Meta:
        model = InstantOfferModel
        fields = '__all__'


class AmazingPanelSerializers(serializers.ModelSerializer):
    class Meta:
        model = AmazingOfferModel
        fields = '__all__'


class AsemblePanelSerializers(serializers.ModelSerializer):
    class Meta:
        model = AsemblePanelModel
        fields = '__all__'


class DailyWorksSerializers(serializers.ModelSerializer):
    class Meta:
        model = DailyWorksModel
        fields = '__all__'


class FinancialStatementSerializers(serializers.ModelSerializer):
    class Meta:
        model = DailyWorksModel
        fields = '__all__'


class FaqSerializers(serializers.ModelSerializer):
    class Meta:
        model = FaqQuestionModel
        fields = '__all__'


class AmazingOfferSerializers(serializers.ModelSerializer):
    class Meta:
        model = AmazingOfferModel
        fields = '__all__'


class SuggestedProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = SuggestedProductsModel
        fields = '__all__'


class ContractUsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ContactUsModel
        fields = '__all__'
