from django.db import models
from django_jalali.db import models as jmodels
from django.shortcuts import reverse
from apps.user.models import UserModel
from django.core.validators import MaxValueValidator, MinValueValidator


# This Model is main category for all products and child categories base parent
class MainCategoryModel(models.Model):
    title = models.CharField(max_length=1000, verbose_name='عنوان')
    url = models.SlugField(unique=True, allow_unicode=True, verbose_name='لینک')
    active = models.BooleanField(default=True, verbose_name='فعال')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product:products_main_category', args=[self.url])


class MainCategoryImageModel(models.Model):
    main_category = models.OneToOneField(MainCategoryModel, on_delete=models.CASCADE, related_name='main_category_image'
                                         , verbose_name='دسته بندی اصلی')
    image = models.ImageField(upload_to='product/category', verbose_name='تصویر')
    description = models.TextField(verbose_name='توضیحات')


# This Model is child category and this models each category can be a parent from child category
class ChildCategoryModel(models.Model):
    title = models.CharField(max_length=1000, verbose_name='عنوان')
    url = models.SlugField(unique=True, allow_unicode=True, verbose_name='لینک')
    base_category = models.ForeignKey(to=MainCategoryModel, on_delete=models.CASCADE,
                                      related_name='base_category_child', verbose_name='دسته بندی اصلی')
    parent_category = models.ForeignKey(to='ChildCategoryModel', on_delete=models.CASCADE,
                                        related_name='child_category', null=True, blank=True,
                                        verbose_name='دسته بندی پدر')
    active = models.BooleanField(default=True, verbose_name='فعال')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product:products_child_category', args=[self.url])


class ChildCategoryImageModel(models.Model):
    child_category = models.OneToOneField(ChildCategoryModel, on_delete=models.CASCADE,
                                          related_name='child_category_image', verbose_name='دسته بندی فرزند')
    image = models.ImageField(upload_to='product/category', verbose_name='')
    description = models.TextField(verbose_name='')


class BrandModel(models.Model):
    title = models.CharField(max_length=1000, verbose_name='عنوان')
    image = models.ImageField(upload_to='product/brands_image', verbose_name='تصویر')
    url = models.SlugField(unique=True, allow_unicode=True, verbose_name='لینک')
    description = models.TextField(verbose_name='توضیحات')
    active = models.BooleanField(default=True, verbose_name='فعال')
    category = models.ManyToManyField(ChildCategoryModel, related_name='category_brands', verbose_name='دسته بندی')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        pass


class ProductPriceChartModel(models.Model):
    product = models.ForeignKey('ProductModel', on_delete=models.CASCADE, related_name='product_price_chart',
                                verbose_name='کالا')
    price = models.IntegerField(verbose_name='قیمت')
    date = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ')


class ProductModel(models.Model):
    title = models.CharField(max_length=1000, verbose_name='عنوان')
    main_category = models.ForeignKey(to=MainCategoryModel, on_delete=models.DO_NOTHING,
                                      related_name='main_category_products', verbose_name='دسته بندی اصلی')
    child_category = models.ForeignKey(to=ChildCategoryModel, on_delete=models.DO_NOTHING,
                                       related_name='child_category_products', verbose_name='دسته بندی فرزند')
    brand = models.ForeignKey(to=BrandModel, on_delete=models.DO_NOTHING, related_name='brands_products',
                              verbose_name='برند')
    description = models.TextField(verbose_name='توضیحات')
    url = models.SlugField(unique=True, allow_unicode=True, verbose_name='لینک')
    image = models.ImageField(upload_to='product/product_images', verbose_name='تصویر')
    published_date = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')
    update_date = jmodels.jDateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    price_after_off = models.PositiveIntegerField(null=True, blank=True, verbose_name='قیمت بعد از تخفیف')
    view_num = models.PositiveIntegerField(verbose_name='تعداد بازدید')
    off = models.PositiveIntegerField(default=0, verbose_name='تخفیف')
    sell = models.PositiveIntegerField(default=0, verbose_name='تعداد فروش')
    active = models.BooleanField(default=False, verbose_name='فعال')
    available = models.BooleanField(default=True, verbose_name='موجودی')

    def get_absolute_url(self):
        return reverse('product:product_detail_view', args=[self.url])

    def save(self, *args, **kwargs):
        self.price_after_off = self.price * (100 - self.off) / 100
        super().save(*args, **kwargs)
        ProductPriceChartModel.objects.get_or_create(product_id=self.id, price=self.price_after_off)

    def __str__(self):
        return self.title


class CategoryFiledModel(models.Model):
    title = models.CharField(max_length=1000, verbose_name='عنوان')
    category = models.ManyToManyField(to=ChildCategoryModel, related_name='child_category_field',
                                      verbose_name='دسته بندی')

    def __str__(self):
        return self.title


class ProductFieldModel(models.Model):
    field = models.ForeignKey(to=CategoryFiledModel, on_delete=models.CASCADE, related_name='category_fields',
                              verbose_name='فیلد')
    product = models.ForeignKey(to=ProductModel, on_delete=models.CASCADE, related_name='product_fields',
                                verbose_name='کالا')
    amount = models.TextField(verbose_name='مقدار')


class ProductImageModel(models.Model):
    product = models.ForeignKey(to=ProductModel, on_delete=models.CASCADE, related_name='product_images',
                                verbose_name='کالا')
    image = models.ImageField(upload_to='product/product_images', verbose_name='تصویر')


class ProductVideoModel(models.Model):
    product = models.ForeignKey(to=ProductModel, on_delete=models.CASCADE, related_name='product_video',
                                verbose_name='کالا')
    video = models.ImageField(upload_to='product/product_videos', verbose_name='ویدیو')


class ProductCommentModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, related_name='user_product_comments',
                             verbose_name='کاربر')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='product_comments',
                                verbose_name='کالا')
    text = models.TextField(verbose_name='متن')
    published_date = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')
    edit_date = jmodels.jDateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    active = models.BooleanField(default=False, verbose_name='وضعیت')
    admin_seen = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, related_name='admin_seen_product_comments',
                                   null=True, blank=True, verbose_name='بررسی ادمین')
    admin_solve = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, related_name='admin_solve_product_comments',
                                    null=True, blank=True)
    admin_solve_text = models.TextField(null=True, blank=True)
    grade = models.PositiveIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    like_num = models.PositiveIntegerField(default=0)
    dislike_num = models.PositiveIntegerField(default=0)



class ProductCommentPositivePointsView(models.Model):
    comment = models.OneToOneField(ProductCommentModel, on_delete=models.CASCADE,
                                   related_name='comment_positive_points')
    text = models.TextField()

    def get_list(self):
        return self.text.split(',')


class ProductCommentNegativePointsView(models.Model):
    comment = models.OneToOneField(ProductCommentModel, on_delete=models.CASCADE,
                                   related_name='comment_negative_points')
    text = models.TextField()

    def get_list(self):
        return self.text.split(',')


class UserFavoriteProductModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user_favorite_product',
                             verbose_name='کاربر')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='favorite_product',
                                verbose_name='کالا')


class ProductViewModel(models.Model):
    ip = models.CharField(max_length=100, verbose_name='ای پی')
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, related_name='user_product_view', null=True,
                             blank=True, verbose_name='کاربر')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='product_view',
                                verbose_name='محصول')
    date_view = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ بازدید')


# -----------------------------------------------------Special Models---------------------------------------------------
class CpuPlatformModel(models.Model):
    title = models.CharField(max_length=1000, unique=True, verbose_name='عنوان')

    def __str__(self):
        return self.title


class GpuPlatformModel(models.Model):
    title = models.CharField(max_length=1000, unique=True, verbose_name='عنوان')

    def __str__(self):
        return self.title


class FanCpuPlatformModel(models.Model):
    title = models.CharField(max_length=1000, unique=True, verbose_name='عنوان')

    def __str__(self):
        return self.title


class SocketTypeModel(models.Model):
    title = models.CharField(max_length=1000, unique=True, verbose_name='عنوان')

    def __str__(self):
        return self.title


class DDRModel(models.Model):
    title = models.CharField(max_length=1000, unique=True, verbose_name='عنوان')

    def __str__(self):
        return self.title


class GpuDDRModel(models.Model):
    title = models.CharField(max_length=1000, unique=True, verbose_name='عنوان')

    def __str__(self):
        return self.title


class SeriesModel(models.Model):
    title = models.CharField(max_length=1000, unique=True ,verbose_name='عنوان')

    def __str__(self):
        return self.title


class BitTypeModel(models.Model):
    title = models.CharField(max_length=1000, unique=True ,verbose_name='عنوان')

    def __str__(self):
        return self.title


class CpuCoreModel(models.Model):
    title = models.CharField(max_length=1000, unique=True, verbose_name='عنوان')

    def __str__(self):
        return self.title


class OnBoardGpuModel(models.Model):
    title = models.CharField(max_length=1000, unique=True, verbose_name='عنوان')

    def __str__(self):
        return self.title


class FormFactorModel(models.Model):
    title = models.CharField(max_length=1000, unique=True, verbose_name='عنوان')

    def __str__(self):
        return self.title


class MainBoardChipSetModel(models.Model):
    title = models.CharField(max_length=1000, unique=True, verbose_name='عنوان')

    def __str__(self):
        return self.title


class RamFrequencyModel(models.Model):
    title = models.CharField(max_length=1000, unique=True, verbose_name='عنوان')

    def __str__(self):
        return self.title


class RamPlatformModel(models.Model):
    title = models.CharField(max_length=1000, unique=True, verbose_name='عنوان')

    def __str__(self):
        return self.title


class HardTypeModel(models.Model):
    title = models.CharField(max_length=1000, unique=True, verbose_name='عنوان')

    def __str__(self):
        return self.title


class SSDTypeModel(models.Model):
    title = models.CharField(max_length=1000, unique=True, verbose_name='عنوان')

    def __str__(self):
        return self.title


class SataTypeModel(models.Model):
    title = models.CharField(max_length=1000, unique=True, verbose_name='عنوان')

    def __str__(self):
        return self.title


class PowerFormFactorModel(models.Model):
    title = models.CharField(max_length=1000, unique=True, verbose_name='عنوان')

    def __str__(self):
        return self.title


class LaptopCpuModel(models.Model):
    title = models.CharField(max_length=10000, unique=True, verbose_name='پردازنده')

    def __str__(self):
        return self.title


class LaptopRamModel(models.Model):
    title = models.CharField(max_length=10000, unique=True, verbose_name='رم')

    def __str__(self):
        return self.title


class LaptopSSDModel(models.Model):
    title = models.CharField(max_length=10000, unique=True, verbose_name='اس اس دی')

    def __str__(self):
        return self.title


class LaptopHardModel(models.Model):
    title = models.CharField(max_length=10000, unique=True, verbose_name='هارد')

    def __str__(self):
        return self.title


class LaptopGpuModel(models.Model):
    title = models.CharField(max_length=10000, unique=True, verbose_name='گرافیک')

    def __str__(self):
        return self.title


class LaptopGpuStorageModel(models.Model):
    title = models.CharField(max_length=10000, unique=True, verbose_name='حافظه گرافیک')

    def __str__(self):
        return self.title


class LaptopScreenSizeModel(models.Model):
    title = models.CharField(max_length=10000, unique=True, verbose_name='سایز صفحه نمایش')

    def __str__(self):
        return self.title


class LaptopResolutionModel(models.Model):
    title = models.CharField(max_length=10000, unique=True, verbose_name='رزولوشن')

    def __str__(self):
        return self.title


class CpuModel(ProductModel):
    platform = models.ForeignKey(CpuPlatformModel, on_delete=models.DO_NOTHING, related_name='platform_cpus',
                                 verbose_name='پلتقرم')
    socket = models.ForeignKey(SocketTypeModel, on_delete=models.DO_NOTHING, related_name='socket_cpus',
                               verbose_name='سوکت')
    ddr = models.ManyToManyField(DDRModel, related_name='ddr_cpus', verbose_name='نسل رم')
    series = models.ForeignKey(SeriesModel, on_delete=models.DO_NOTHING, related_name='series_cpus',
                               verbose_name='سری')
    bit = models.ForeignKey(BitTypeModel, on_delete=models.DO_NOTHING, related_name='bit_cpus', verbose_name='بیت')
    core = models.ForeignKey(CpuCoreModel, on_delete=models.DO_NOTHING, related_name='core_cpus',
                             verbose_name='تعداد هسته')
    gpu = models.ForeignKey(OnBoardGpuModel, on_delete=models.DO_NOTHING, related_name='on_board', null=True,
                            blank=True, verbose_name='گرافیک')
    speed = models.CharField(max_length=1000, verbose_name='سرعت')
    unlocked = models.BooleanField(verbose_name='آنلاک')
    threads = models.CharField(max_length=1000, verbose_name='رشته')
    cache = models.CharField(max_length=1000, verbose_name='کش')
    tdp = models.PositiveIntegerField(verbose_name='توان مصرفی')
    boost_frequency = models.CharField(max_length=1000, verbose_name='فرکانس بوست')
    architecture_size = models.CharField(max_length=1000, verbose_name='معماری اندازه')

    def save(self, *args, **kwargs):
        main_category, status = MainCategoryModel.objects.get_or_create(title='کامپیوتر', url='computer', active=True)
        category, status = ChildCategoryModel.objects.get_or_create(title='قطعات کامپیوتری', url='computer-parts',
                                                                    base_category=main_category, active=True)
        child_category, status = ChildCategoryModel.objects.get_or_create(title='پردازنده', url='cpu',
                                                                          base_category=main_category,
                                                                          parent_category=category, active=True)
        self.main_category = main_category
        self.child_category = child_category
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class MainBoardModel(ProductModel):
    socket = models.ForeignKey(SocketTypeModel, on_delete=models.DO_NOTHING, related_name='socket_main_boards',
                               verbose_name='سوکت')
    ddr = models.ForeignKey(DDRModel, on_delete=models.DO_NOTHING, related_name='ddr_main_boards',
                            verbose_name='نسل رم')
    form_factor = models.ForeignKey(FormFactorModel, on_delete=models.DO_NOTHING,
                                    related_name='form_factor_main_boards', verbose_name='فرم فاکتور')
    has_wifi = models.BooleanField(verbose_name='وای فای')
    has_bluetooth = models.BooleanField(verbose_name='بلوتوث')
    chipset = models.ForeignKey(MainBoardChipSetModel, on_delete=models.DO_NOTHING, related_name='chipset_main_boards',
                                verbose_name='چیپست')
    number_of_ram_slot = models.PositiveIntegerField(verbose_name='تعداد اسلات رم')
    platform = models.ForeignKey(CpuPlatformModel, on_delete=models.DO_NOTHING, related_name='platform_main_boards',
                                 verbose_name='پلتفرم')
    dimensions = models.CharField(max_length=1000, verbose_name='ابعاد')
    has_hdmi_port = models.BooleanField(verbose_name='پورت hdmi')
    has_vga_port = models.BooleanField(verbose_name='پورت vga')
    has_display_port = models.BooleanField(verbose_name='پورت display')
    voice_card = models.CharField(max_length=1000, verbose_name='کارت صدا')
    usb_ports = models.CharField(max_length=1000, verbose_name='پورت usb')
    lan_port = models.CharField(max_length=1000, verbose_name='پورت lan')
    jack_3_5 = models.CharField(max_length=1000, verbose_name='جک 3.5')
    pci_slots = models.CharField(max_length=1000, verbose_name='اسلات pci')
    power_connector = models.CharField(max_length=1000, verbose_name='کانکتور پاور')
    ram_frequency = models.ManyToManyField(RamFrequencyModel, related_name='ram_frequency_main_boards',
                                           verbose_name='فرکانس رم')

    def save(self, *args, **kwargs):
        main_category, status = MainCategoryModel.objects.get_or_create(title='کامپیوتر', url='computer', active=True)
        category, status = ChildCategoryModel.objects.get_or_create(title='قطعات کامپیوتری', url='computer-parts',
                                                                    base_category=main_category, active=True)
        child_category, status = ChildCategoryModel.objects.get_or_create(title='مادربرد', url='main-board',
                                                                          base_category=main_category,
                                                                          parent_category=category, active=True)
        self.main_category = main_category
        self.child_category = child_category
        self.price_after_off = self.price * (100 - self.off) / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class GpuModel(ProductModel):
    platform = models.ForeignKey(GpuPlatformModel, on_delete=models.DO_NOTHING, related_name='platform_gpus',
                                 verbose_name='پلتفرم')
    ddr = models.ForeignKey(GpuDDRModel, on_delete=models.DO_NOTHING, related_name='ddr_gpus', verbose_name='نسل رم')
    storage_bus = models.CharField(max_length=1000, verbose_name='باس حافظه')
    core_frequency = models.CharField(max_length=10000, verbose_name='فرکانس هسته')
    storage_frequency = models.CharField(max_length=1000, verbose_name='فرکانس حافظه')
    power_usage = models.CharField(max_length=1000, verbose_name='نوان مصرفی')
    suggested_power = models.CharField(max_length=1000, verbose_name='پاور پیشنهادی')
    power_connectors = models.CharField(max_length=1000, verbose_name='کانکنور پاور')
    Hdmi_port = models.PositiveIntegerField(verbose_name='پورت hdmi')
    display_port = models.PositiveIntegerField(verbose_name='پورت display')
    mini_display_port = models.PositiveIntegerField(verbose_name='پورت mini display')
    dvi_port = models.PositiveIntegerField(verbose_name='پورت dvi')
    vga_port = models.PositiveIntegerField(verbose_name='پورت vga')
    type_c_port = models.PositiveIntegerField(verbose_name='پورت type c')
    direct_x = models.CharField(max_length=1000, verbose_name='دایرکت x')
    multi_gpu = models.BooleanField(verbose_name='مولتی گرافیک')
    resolution = models.CharField(max_length=1000, verbose_name='رزولیشن')

    def save(self, *args, **kwargs):
        main_category, status = MainCategoryModel.objects.get_or_create(title='کامپیوتر', url='computer', active=True)
        category, status = ChildCategoryModel.objects.get_or_create(title='قطعات کامپیوتری', url='computer-parts',
                                                                    base_category=main_category, active=True)
        child_category, status = ChildCategoryModel.objects.get_or_create(title='کارت گرافیک', url='gpu',
                                                                          base_category=main_category,
                                                                          parent_category=category, active=True)
        self.main_category = main_category
        self.child_category = child_category
        self.price_after_off = self.price * (100 - self.off) / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class FanCpuModel(ProductModel):
    platform = models.ManyToManyField(FanCpuPlatformModel, related_name='platform_fan_cpus', verbose_name='پلتفرم')
    weight = models.CharField(max_length=1000, verbose_name='وزن')
    dimensions = models.CharField(max_length=1000, verbose_name='ابعاد')
    radiator_material = models.CharField(max_length=1000, verbose_name='جنس رادیاتور')
    sockets = models.ManyToManyField(SocketTypeModel, related_name='socket_fan_cpus', verbose_name='سوکت')
    fan_size = models.CharField(max_length=1000, verbose_name='سایز فن')
    power_usage = models.CharField(max_length=1000, verbose_name='توان مصرفی')
    tdp = models.PositiveIntegerField(verbose_name='توان tdp')

    def save(self, *args, **kwargs):
        main_category, status = MainCategoryModel.objects.get_or_create(title='کامپیوتر', url='computer', active=True)
        category, status = ChildCategoryModel.objects.get_or_create(title='قطعات کامپیوتری', url='computer-parts',
                                                                    base_category=main_category, active=True)
        child_category, status = ChildCategoryModel.objects.get_or_create(title='خنک کننده پردازنده', url='fan-cpu',
                                                                          base_category=main_category,
                                                                          parent_category=category, active=True)
        self.main_category = main_category
        self.child_category = child_category
        self.price_after_off = self.price * (100 - self.off) / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class RamModel(ProductModel):
    platform = models.ForeignKey(RamPlatformModel, on_delete=models.DO_NOTHING, related_name='platform_rams',
                                 verbose_name='پلتفرم')
    ddr = models.ForeignKey(DDRModel, on_delete=models.DO_NOTHING, related_name='ddr_rams', verbose_name='نسل رم')
    number_of_module = models.PositiveIntegerField(verbose_name='تعداد ماژول ')
    storage = models.CharField(max_length=1000, verbose_name='حافظه')
    frequency = models.ForeignKey(RamFrequencyModel, on_delete=models.DO_NOTHING, related_name='frequency_rams',
                                  verbose_name='فرکانس')
    cl_number = models.CharField(max_length=1000, verbose_name='شماره cl')
    number_of_pin = models.CharField(max_length=1000, verbose_name='تعداد پین')
    timing = models.CharField(max_length=1000, verbose_name='تایمینگ')
    number_of_channels = models.CharField(max_length=1000, verbose_name='تعداد کانال')
    has_rgb = models.BooleanField(verbose_name='دارای rgb')

    def save(self, *args, **kwargs):
        main_category, status = MainCategoryModel.objects.get_or_create(title='کامپیوتر', url='computer', active=True)
        category, status = ChildCategoryModel.objects.get_or_create(title='قطعات کامپیوتری', url='computer-parts',
                                                                    base_category=main_category, active=True)
        child_category, status = ChildCategoryModel.objects.get_or_create(title='رم', url='ram',
                                                                          base_category=main_category,
                                                                          parent_category=category, active=True)
        self.main_category = main_category
        self.child_category = child_category
        self.price_after_off = self.price * (100 - self.off) / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class HardModel(ProductModel):
    type = models.ForeignKey(HardTypeModel, on_delete=models.DO_NOTHING, related_name='hard_types', verbose_name='نوع')
    dimensions = models.CharField(max_length=1000, verbose_name='ابعاد')
    head_size = models.CharField(max_length=1000, verbose_name='سایز هد')
    storage = models.CharField(max_length=1000, verbose_name='حافظه')
    sata = models.ForeignKey(SataTypeModel, on_delete=models.DO_NOTHING, related_name='sata_hard', verbose_name='ساتا')
    cache = models.CharField(max_length=1000, verbose_name='کش')
    rotor_speed = models.CharField(max_length=1000, verbose_name='سرعت روتور')
    water_proof = models.BooleanField(verbose_name='ضد آب')
    weight = models.CharField(max_length=1000, verbose_name='وزن')
    noise_level = models.CharField(max_length=1000, verbose_name='سطح نویز')
    power_usage = models.CharField(max_length=1000, verbose_name='توان مصرفی')
    frequency_limit = models.CharField(max_length=1000, verbose_name='بازه فرکانس')

    def save(self, *args, **kwargs):
        main_category, status = MainCategoryModel.objects.get_or_create(title='کامپیوتر', url='computer', active=True)
        category, status = ChildCategoryModel.objects.get_or_create(title='قطعات کامپیوتری', url='computer-parts',
                                                                    base_category=main_category, active=True)
        child_category, status = ChildCategoryModel.objects.get_or_create(title='هارد', url='hard',
                                                                          base_category=main_category,
                                                                          parent_category=category, active=True)
        self.main_category = main_category
        self.child_category = child_category
        self.price_after_off = self.price * (100 - self.off) / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class SSDModel(ProductModel):
    type = models.ForeignKey(SSDTypeModel, on_delete=models.DO_NOTHING, related_name='ssd_type', verbose_name='نوع')
    read_speed = models.CharField(max_length=1000, verbose_name='سرعت خوانندن')
    write_speed = models.CharField(max_length=1000, verbose_name='سرعت نوشتن')
    storage = models.CharField(max_length=1000, verbose_name='حافظه')
    head_sing = models.BooleanField(verbose_name='هیدسینگ')

    def save(self, *args, **kwargs):
        main_category, status = MainCategoryModel.objects.get_or_create(title='کامپیوتر', url='computer', active=True)
        category, status = ChildCategoryModel.objects.get_or_create(title='قطعات کامپیوتری', url='computer-parts',
                                                                    base_category=main_category, active=True)
        child_category, status = ChildCategoryModel.objects.get_or_create(title='اس اس دی', url='ssd',
                                                                          base_category=main_category,
                                                                          parent_category=category, active=True)
        self.main_category = main_category
        self.child_category = child_category
        self.price_after_off = self.price * (100 - self.off) / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PowerModel(ProductModel):
    output_power = models.PositiveIntegerField(verbose_name='توان خروجی')
    form_factor = models.ForeignKey(PowerFormFactorModel, on_delete=models.DO_NOTHING,
                                    related_name='form_factor_powers', verbose_name='فرم فاکنور')
    dimensions = models.CharField(max_length=1000, verbose_name='ابعاد')
    weight = models.CharField(max_length=1000, verbose_name='وزن')
    modular = models.BooleanField(verbose_name='ماژولار')
    standard_certificate = models.CharField(max_length=1000, verbose_name='گواهینامه استاندارد')
    limit_frequency = models.CharField(max_length=1000, verbose_name='محدوده فرکانس')
    output_ports = models.CharField(max_length=1000, verbose_name='پورت های خروجی')

    def save(self, *args, **kwargs):
        main_category, status = MainCategoryModel.objects.get_or_create(title='کامپیوتر', url='computer', active=True)
        category, status = ChildCategoryModel.objects.get_or_create(title='قطعات کامپیوتری', url='computer-parts',
                                                                    base_category=main_category, active=True)
        child_category, status = ChildCategoryModel.objects.get_or_create(title='پاور', url='power',
                                                                          base_category=main_category,
                                                                          parent_category=category, active=True)
        self.main_category = main_category
        self.child_category = child_category
        self.price_after_off = self.price * (100 - self.off) / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CaseModel(ProductModel):
    material = models.CharField(max_length=1000, verbose_name='جنس')
    dimensions = models.CharField(max_length=1000, verbose_name='ابعاد')
    weight = models.CharField(max_length=1000, verbose_name='وزن')
    main_board_form_factor = models.ManyToManyField(FormFactorModel, related_name='form_factor_cases',
                                                    verbose_name='فرم فاکتور مادربرد')
    power_form_factor = models.ManyToManyField(PowerFormFactorModel, related_name='power_form_cases',
                                               verbose_name='فرم فاکتور پاور')
    gpu_space = models.CharField(max_length=1000, verbose_name='فضای کارت گرافیک')
    case_fan_details = models.CharField(max_length=1000, verbose_name='اطلاعات فن کیس')

    def save(self, *args, **kwargs):
        main_category, status = MainCategoryModel.objects.get_or_create(title='کامپیوتر', url='computer', active=True)
        category, status = ChildCategoryModel.objects.get_or_create(title='قطعات کامپیوتری', url='computer-parts',
                                                                    base_category=main_category, active=True)
        child_category, status = ChildCategoryModel.objects.get_or_create(title='کیس', url='case',
                                                                          base_category=main_category,
                                                                          parent_category=category, active=True)
        self.main_category = main_category
        self.child_category = child_category
        self.price_after_off = self.price * (100 - self.off) / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class OpticalDriveModel(ProductModel):
    pass


class AssembledCaseModel(ProductModel):
    cpu = models.ManyToManyField(CpuModel, verbose_name='پردازنده')
    main_board = models.ForeignKey(MainBoardModel, related_name='main_board_assembled_cases', on_delete=models.DO_NOTHING, verbose_name='مادربرد')
    gpu = models.ManyToManyField(GpuModel, blank=True, verbose_name='کارت گرافیک')
    fan_cpu = models.ManyToManyField(FanCpuModel, verbose_name='فن پردازنده')
    ram = models.ManyToManyField(RamModel, verbose_name='رم')
    hard = models.ManyToManyField(HardModel, blank=True, verbose_name='هارد')
    ssd = models.ManyToManyField(SSDModel, blank=True, verbose_name='')
    power = models.ForeignKey(PowerModel, on_delete=models.DO_NOTHING, verbose_name='پاور')
    case = models.ForeignKey(CaseModel, on_delete=models.DO_NOTHING, verbose_name='کیس')
    optical_drive = models.ManyToManyField(OpticalDriveModel, blank=True, verbose_name='درایو نوری')

    def save(self, *args, **kwargs):
        main_category, status = MainCategoryModel.objects.get_or_create(title='کامپیوتر', url='computer', active=True)
        child_category, status = ChildCategoryModel.objects.get_or_create(title='کیس های اسمبل شده', url='assembled-cases',
                                                                    base_category=main_category, active=True)

        self.main_category = main_category
        self.child_category = child_category
        self.price_after_off = self.price * (100 - self.off) / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class LaptopModel(ProductModel):
    cpu = models.ForeignKey(LaptopCpuModel, on_delete=models.DO_NOTHING, verbose_name='پردازنده')
    ram = models.ForeignKey(LaptopRamModel, on_delete=models.DO_NOTHING, verbose_name='رم')
    ssd = models.ForeignKey(LaptopSSDModel, on_delete=models.DO_NOTHING, verbose_name='اس اس دی')
    hard = models.ForeignKey(LaptopHardModel, on_delete=models.DO_NOTHING, verbose_name='هارد')
    gpu = models.ForeignKey(LaptopGpuModel, on_delete=models.DO_NOTHING, verbose_name='گرافیک')
    on_site_gpu = models.BooleanField(verbose_name='گرافیک مجزا')
    gpu_storage = models.ForeignKey(LaptopGpuStorageModel, on_delete=models.DO_NOTHING, verbose_name='حافظه پردازنده گرافیکی')
    screen_size = models.ForeignKey(LaptopScreenSizeModel, on_delete=models.DO_NOTHING, verbose_name='ابعاد صفحه نمایش')
    resolution = models.ForeignKey(LaptopResolutionModel, on_delete=models.DO_NOTHING, verbose_name='رزولوشن')
    weight = models.FloatField(verbose_name='وزن')
    battery_storage = models.PositiveIntegerField(verbose_name='ظرفیت باتری')
    power_adaptor = models.PositiveIntegerField(verbose_name='اداپتور پاور')


class AllInOneModel(ProductModel):
    pass


class KeyBoardModel(ProductModel):
    pass


class MouseModel(ProductModel):
    pass


class SpeakerModel(ProductModel):
    pass


class MonitorModel(ProductModel):
    pass
