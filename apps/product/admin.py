from django.contrib import admin
from .models import *


@admin.register(MainCategoryModel)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'active']
    prepopulated_fields = {'url': ('title', )}


@admin.register(MainCategoryImageModel)
class MainCategoryImageAdmin(admin.ModelAdmin):
    list_display = ['main_category']


@admin.register(ChildCategoryModel)
class ChildCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'base_category', 'parent_category', 'active']
    prepopulated_fields = {'url': ('title', )}


@admin.register(BrandModel)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'url', 'active']
    prepopulated_fields = {'url': ('title', )}


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand', 'url', 'image', 'published_date']
    prepopulated_fields = {'url': ('title', )}


@admin.register(CategoryFiledModel)
class CategoryFieldAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(ProductFieldModel)
class ProductFieldAdmin(admin.ModelAdmin):
    list_display = ['product', 'amount']


@admin.register(ProductViewModel)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ['product']


@admin.register(ProductImageModel)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']


@admin.register(ProductCommentModel)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(UserFavoriteProductModel)
class ProductFavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']


@admin.register(CpuPlatformModel)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(GpuPlatformModel)
class GpuPlatformAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(FanCpuPlatformModel)
class FanCpuPlatformAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(SocketTypeModel)
class SocketAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(DDRModel)
class DDRAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(GpuDDRModel)
class GpuDDRAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(SeriesModel)
class SeriesAdmin(admin.ModelAdmin):
    list_display = []


@admin.register(BitTypeModel)
class BitAdmin(admin.ModelAdmin):
    list_display = []


@admin.register(OnBoardGpuModel)
class OnBoardAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(CpuModel)
class CpuAdmin(admin.ModelAdmin):
    list_display = ['socket']


@admin.register(CpuCoreModel)
class CpuCoreAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(FormFactorModel)
class FormFactorAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(MainBoardChipSetModel)
class MainBoardChipSetAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(RamFrequencyModel)
class RamFrequencyAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(HardTypeModel)
class HardTypeAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(SataTypeModel)
class SataTypeAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(PowerFormFactorModel)
class PowerFormFactorAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(ProductPriceChartModel)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ['product']


@admin.register(MainBoardModel)
class MainBoardAdmin(admin.ModelAdmin):
    list_display = ['socket']


@admin.register(GpuModel)
class GpuAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(FanCpuModel)
class FanCpuAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(RamPlatformModel)
class RamPlatformAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(RamModel)
class RamAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(HardModel)
class HardAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(SSDModel)
class SSDAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(PowerModel)
class PowerAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(CaseModel)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(LaptopCpuModel)
class LaptopCpuAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(LaptopGpuModel)
class LaptopGpuAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(LaptopGpuStorageModel)
class LaptopGpuStorageAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(LaptopRamModel)
class LaptopRamAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(LaptopSSDModel)
class LaptopSSDAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(LaptopHardModel)
class LaptopHardAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(AssembledCaseModel)
class AssembledAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(LaptopModel)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ['title']
