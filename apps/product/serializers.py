from rest_framework import serializers
from .models import *

class MainCategorySerializers(serializers.ModelSerializer):
    base_category_child = serializers.StringRelatedField(many=True)

    class Meta:
        model = MainCategoryModel
        fields = '__all__'


class MainCategoryImageSerializers(serializers.ModelSerializer):
    main_category = serializers.StringRelatedField()

    class Meta:
        model = MainCategoryImageModel
        fields = '__all__'


class ChildCategorySerializers(serializers.ModelSerializer):
    child_category_image = serializers.StringRelatedField()

    class Meta:
        model = ChildCategoryModel
        fields = '__all__'


class ChildCategoryImageSerializers(serializers.ModelSerializer):
    child_category = serializers.StringRelatedField()

    class Meta:
        model = ChildCategoryModel
        fields = '__all__'


class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = BrandModel
        fields = '__all__'


class ProductSerializers(serializers.ModelSerializer):
    main_category = serializers.StringRelatedField()
    child_category = serializers.StringRelatedField()
    class Meta:
        model = ProductModel
        fields = '__all__'


class CategoryFieldSerializers(serializers.ModelSerializer):
    class Meta:
        model = CategoryFiledModel
        fields = '__all__'


class ProductFieldSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductFieldModel
        fields = '__all__'


class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImageModel
        fields = '__all__'



class ProductVideoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImageModel
        fields = '__all__'


class ProductCommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductCommentModel
        fields = '__all__'


class UserFavoriteProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserFavoriteProductModel
        fields = '__all__'


class ProductViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductViewModel
        fields = '__all__'


class CpuPlatformSerializers(serializers.ModelSerializer):
    class Meta:
        model = CpuPlatformModel
        fields = '__all__'


class GpuPlatformSerializers(serializers.ModelSerializer):
    class Meta:
        model = GpuPlatformModel
        fields = '__all__'


class FanCpuPlatformSerializers(serializers.ModelSerializer):
    class Meta:
        model = FanCpuPlatformModel
        fields = '__all__'


class SocketTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = SocketTypeModel
        fields = '__all__'


class DDRSerializers(serializers.ModelSerializer):
    class Meta:
        model = DDRModel
        fields = '__all__'


class GpuDDRSerializers(serializers.ModelSerializer):
    class Meta:
        model = GpuDDRModel
        fields = '__all__'


class SeriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = SeriesModel
        fields = '__all__'


class BitTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = BitTypeModel
        fields = '__all__'


class CpuCoreSerializers(serializers.ModelSerializer):
    class Meta:
        model = CpuCoreModel
        fields = '__all__'


class OnBoardGpuSerializers(serializers.ModelSerializer):
    class Meta:
        model = OnBoardGpuModel
        fields = '__all__'


class FormFactorSerializers(serializers.ModelSerializer):
    class Meta:
        model = FormFactorModel
        fields = '__all__'


class MainBoardChipsetSerializers(serializers.ModelSerializer):
    class Meta:
        model = MainBoardChipSetModel
        fields = '__all__'


class RamFrequencySerializers(serializers.ModelSerializer):
    class Meta:
        model = RamFrequencyModel
        fields = '__all__'


class RamPlatformSerializers(serializers.ModelSerializer):
    class Meta:
        model = RamPlatformModel
        fields = '__all__'


class HardTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = HardTypeModel
        fields = '__all__'


class SSDTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = SSDTypeModel
        fields = '__all__'


class SataTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = SataTypeModel
        fields = '__all__'


class PowerFormFactorSerializers(serializers.ModelSerializer):
    class Meta:
        model = PowerFormFactorModel
        fields = '__all__'


class CpuSerializers(serializers.ModelSerializer):
    class Meta:
        model = CpuModel
        fields = '__all__'


class MainBoardSerializers(serializers.ModelSerializer):
    class Meta:
        model = MainBoardModel
        fields = '__all__'


class GpuSerializers(serializers.ModelSerializer):
    class Meta:
        model = GpuModel
        fields = '__all__'


class FanCpuSerializers(serializers.ModelSerializer):
    class Meta:
        model = FanCpuModel
        fields = '__all__'


class RamSerializers(serializers.ModelSerializer):
    class Meta:
        model = RamModel
        fields = '__all__'


class HardSerializers(serializers.ModelSerializer):
    class Meta:
        nodel = HardModel
        fields = '__all__'


class SSDSerializers(serializers.ModelSerializer):
    class Meta:
        model = SSDModel
        fields = '__all__'


class PowerSerializers(serializers.ModelSerializer):
    class Meta:
        model = PowerModel
        fields = '__all__'


class CaseSerializers(serializers.ModelSerializer):
    class Meta:
        model = CaseModel
        fields = '__all__'


class KeyBoardSerializers(serializers.ModelSerializer):
    class Meta:
        model = KeyBoardModel
        fields = '__all__'


class MouseSerializers(serializers.ModelSerializer):
    class Meta:
        model = MouseModel
        fields = '__all__'


class SpeakerSerializers(serializers.ModelSerializer):
    class Meta:
        model = SpeakerModel
        fields = '__all__'


class MonitorSerializers(serializers.ModelSerializer):
    class Meta:
        model = MonitorModel
        fields = '__all__'


class OpticalDriveSerializers(serializers.ModelSerializer):
    class Meta:
        model = OpticalDriveModel
        fields = '__all__'
