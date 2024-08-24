from django.db import models
from apps.product.models import ProductModel
from django_jalali.db import models as jmodels
from apps.user.models import UserModel
from apps.product.models import BrandModel
from apps.product.models import ChildCategoryModel
from apps.product.models import ProductCommentModel
from apps.blog.models import BlogCommentModel


banner_order = [(str(i), str(i)) for i in range(1, 5)]

type_banner = [('desktop', 'desktop'), ('phone', 'phone')]


class SiteDetailModel(models.Model):
    title = models.CharField(max_length=10000)
    logo = models.ImageField(upload_to='site_detail/image')
    phone = models.CharField(max_length=11)
    email = models.EmailField()
    address = models.TextField()
    work_time = models.TextField()
    empty_cart_image = models.ImageField(upload_to='site_detail/image')
    footer_title = models.CharField(max_length=1000)
    footer_text = models.TextField()
    about_us_text = models.TextField()
    copy_right = models.TextField()
    enamad_image = models.ImageField(upload_to='site_detail/image', null=True, blank=True)
    enamad_url = models.URLField(null=True, blank=True)
    kasbokar_image = models.ImageField(upload_to='site_detail/image', null=True, blank=True)
    kasbokar_url = models.URLField(null=True, blank=True)
    samandehi_image = models.ImageField(upload_to='site_detail/image', null=True, blank=True)
    samandehi_url = models.URLField(null=True, blank=True)
    limit_of_address_can_add = models.IntegerField()
    suggested_products_image = models.ImageField(upload_to='site_detail/image', null=True, blank=True)
    amazing_products_image = models.ImageField(upload_to='site_detail/image', null=True, blank=True)
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    whatsapp = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)


class AdvertisingBannerModel(models.Model):
    title = models.CharField(max_length=1000)
    url = models.SlugField(unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='panel/banners')
    type = models.CharField(max_length=1000, choices=type_banner)
    order = models.CharField(max_length=1000, choices=banner_order)
    active = models.BooleanField(default=True)


class InstantOfferModel(models.Model):
    product = models.OneToOneField(ProductModel, on_delete=models.CASCADE, related_name='product_instant_offer')
    expired_date = models.DateTimeField()
    active = models.BooleanField(default=True)


class AmazingOfferModel(models.Model):
    product = models.OneToOneField(ProductModel, on_delete=models.CASCADE, related_name='product_amazing_offer')
    expired_date = models.DateTimeField()
    active = models.BooleanField(default=True)


class SuggestedProductsModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='suggested_products')
    order = models.PositiveIntegerField(unique=True)
    active = models.BooleanField(default=True)


class AsemblePanelModel(models.Model):
    main_board_image = models.ImageField(upload_to='panel/asemble_images')
    cpu_image = models.ImageField(upload_to='panel/asemble_images')
    fan_cpu_image = models.ImageField(upload_to='panel/asemble_images')
    ram_image = models.ImageField(upload_to='panel/asemble_images')
    hard_image = models.ImageField(upload_to='panel/asemble_images')
    ssd_image = models.ImageField(upload_to='panel/asemble_images')
    gpu_image = models.ImageField(upload_to='panel/asemble_images')
    optical_drive_image = models.ImageField(upload_to='panel/asemble_images')
    power_image = models.ImageField(upload_to='panel/asemble_images')
    case_image = models.ImageField(upload_to='panel/asemble_images')
    keyboard_image = models.ImageField(upload_to='panel/asemble_images')
    mouse_image = models.ImageField(upload_to='panel/asemble_images')
    speaker_image = models.ImageField(upload_to='panel/asemble_images')
    monitor_image = models.ImageField(upload_to='panel/asemble_images')


class DailyWorksModel(models.Model):
    user = models.ManyToManyField(UserModel, related_name='user_daily_works', )
    title = models.CharField(max_length=10000)
    descriptions = models.TextField(null=True, blank=True)
    date = jmodels.jDateTimeField()


class FinancialStatementModel(models.Model):
    sender_company = models.CharField(max_length=10000)
    receiver_company = models.CharField(max_length=10000)
    sender_address = models.TextField()
    receiver_address = models.TextField()
    sender_post_code = models.CharField(max_length=10, null=True, blank=True)
    receiver_post_code = models.CharField(max_length=10, null=True, blank=True)
    sender_state = models.CharField(max_length=10000, null=True, blank=True)
    receiver_state = models.CharField(max_length=10000, null=True, blank=True)
    sender_city = models.CharField(max_length=10000, null=True, blank=True)
    receiver_city = models.CharField(max_length=10000, null=True, blank=True)
    sender_phone = models.CharField(max_length=11)
    receiver_phone = models.CharField(max_length=11)
    date = models.DateTimeField()
    title = models.CharField(max_length=10000)
    description = models.TextField(null=True, blank=True)


class FinancialStatementObjectsModel(models.Model):
    financial_statement = models.ForeignKey(FinancialStatementModel, on_delete=models.CASCADE, related_name='financial_statement_objects')
    title = models.TextField()
    product_code = models.CharField(max_length=10, null=True, blank=True)
    price = models.PositiveIntegerField()
    off = models.PositiveIntegerField()
    price_after_off = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.price_after_off = self.price * (100 - self.off) / 100
        super().save(*args, **kwargs)


class FaqQuestionModel(models.Model):
    title = models.TextField()
    answer = models.TextField()


class ContactUsModel(models.Model):
    name = models.CharField(max_length=1000)
    family_name = models.CharField(max_length=1000)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    subject = models.TextField()
    message = models.TextField()
