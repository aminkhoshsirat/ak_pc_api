# Generated by Django 4.2.1 on 2024-08-08 17:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BitTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, unique=True, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='BrandModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, verbose_name='عنوان')),
                ('image', models.ImageField(upload_to='product/brands_image', verbose_name='تصویر')),
                ('url', models.SlugField(allow_unicode=True, unique=True, verbose_name='لینک')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('active', models.BooleanField(default=True, verbose_name='فعال')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryFiledModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='ChildCategoryImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product/category', verbose_name='')),
                ('description', models.TextField(verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='ChildCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, verbose_name='عنوان')),
                ('url', models.SlugField(allow_unicode=True, unique=True, verbose_name='لینک')),
                ('active', models.BooleanField(default=True, verbose_name='فعال')),
            ],
        ),
        migrations.CreateModel(
            name='CpuCoreModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, unique=True, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='CpuPlatformModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, unique=True, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='DDRModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, unique=True, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='FanCpuPlatformModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, unique=True, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='FormFactorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, unique=True, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='GpuDDRModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, unique=True, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='GpuPlatformModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, unique=True, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='HardTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, unique=True, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='LaptopCpuModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10000, unique=True, verbose_name='پردازنده')),
            ],
        ),
        migrations.CreateModel(
            name='LaptopGpuModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10000, unique=True, verbose_name='گرافیک')),
            ],
        ),
        migrations.CreateModel(
            name='LaptopGpuStorageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10000, unique=True, verbose_name='حافظه گرافیک')),
            ],
        ),
        migrations.CreateModel(
            name='LaptopHardModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10000, unique=True, verbose_name='هارد')),
            ],
        ),
        migrations.CreateModel(
            name='LaptopRamModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10000, unique=True, verbose_name='رم')),
            ],
        ),
        migrations.CreateModel(
            name='LaptopResolutionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10000, unique=True, verbose_name='رزولوشن')),
            ],
        ),
        migrations.CreateModel(
            name='LaptopScreenSizeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10000, unique=True, verbose_name='سایز صفحه نمایش')),
            ],
        ),
        migrations.CreateModel(
            name='LaptopSSDModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10000, unique=True, verbose_name='اس اس دی')),
            ],
        ),
        migrations.CreateModel(
            name='MainBoardChipSetModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, unique=True, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='MainCategoryImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product/category', verbose_name='تصویر')),
                ('description', models.TextField(verbose_name='توضیحات')),
            ],
        ),
        migrations.CreateModel(
            name='MainCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, verbose_name='عنوان')),
                ('url', models.SlugField(allow_unicode=True, unique=True, verbose_name='لینک')),
                ('active', models.BooleanField(default=True, verbose_name='فعال')),
            ],
        ),
        migrations.CreateModel(
            name='OnBoardGpuModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, unique=True, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='PowerFormFactorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, unique=True, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='متن')),
                ('published_date', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')),
                ('edit_date', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('active', models.BooleanField(default=False, verbose_name='وضعیت')),
                ('admin_solve_text', models.TextField(blank=True, null=True)),
                ('grade', models.PositiveIntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('like_num', models.PositiveIntegerField(default=0)),
                ('dislike_num', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCommentNegativePointsView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ProductCommentPositivePointsView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ProductFieldModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.TextField(verbose_name='مقدار')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product/product_images', verbose_name='تصویر')),
            ],
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, verbose_name='عنوان')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('url', models.SlugField(allow_unicode=True, unique=True, verbose_name='لینک')),
                ('image', models.ImageField(upload_to='product/product_images', verbose_name='تصویر')),
                ('published_date', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')),
                ('update_date', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('price', models.PositiveIntegerField(verbose_name='قیمت')),
                ('price_after_off', models.PositiveIntegerField(blank=True, null=True, verbose_name='قیمت بعد از تخفیف')),
                ('view_num', models.PositiveIntegerField(verbose_name='تعداد بازدید')),
                ('off', models.PositiveIntegerField(default=0, verbose_name='تخفیف')),
                ('sell', models.PositiveIntegerField(default=0, verbose_name='تعداد فروش')),
                ('active', models.BooleanField(default=False, verbose_name='فعال')),
                ('available', models.BooleanField(default=True, verbose_name='موجودی')),
            ],
        ),
        migrations.CreateModel(
            name='ProductPriceChartModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(verbose_name='قیمت')),
                ('date', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ')),
            ],
        ),
        migrations.CreateModel(
            name='ProductVideoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.ImageField(upload_to='product/product_videos', verbose_name='ویدیو')),
            ],
        ),
        migrations.CreateModel(
            name='ProductViewModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=100, verbose_name='ای پی')),
                ('date_view', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ بازدید')),
            ],
        ),
        migrations.CreateModel(
            name='RamFrequencyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, unique=True, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='RamPlatformModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, unique=True, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='SataTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, unique=True, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='SeriesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, unique=True, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='SocketTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, unique=True, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='SSDTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, unique=True, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='AllInOneModel',
            fields=[
                ('productmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.productmodel')),
            ],
            bases=('product.productmodel',),
        ),
        migrations.CreateModel(
            name='AssembledCaseModel',
            fields=[
                ('productmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.productmodel')),
            ],
            bases=('product.productmodel',),
        ),
        migrations.CreateModel(
            name='CaseModel',
            fields=[
                ('productmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.productmodel')),
                ('material', models.CharField(max_length=1000, verbose_name='جنس')),
                ('dimensions', models.CharField(max_length=1000, verbose_name='ابعاد')),
                ('weight', models.CharField(max_length=1000, verbose_name='وزن')),
                ('gpu_space', models.CharField(max_length=1000, verbose_name='فضای کارت گرافیک')),
                ('case_fan_details', models.CharField(max_length=1000, verbose_name='اطلاعات فن کیس')),
            ],
            bases=('product.productmodel',),
        ),
        migrations.CreateModel(
            name='CpuModel',
            fields=[
                ('productmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.productmodel')),
                ('speed', models.CharField(max_length=1000, verbose_name='سرعت')),
                ('unlocked', models.BooleanField(verbose_name='آنلاک')),
                ('threads', models.CharField(max_length=1000, verbose_name='رشته')),
                ('cache', models.CharField(max_length=1000, verbose_name='کش')),
                ('tdp', models.PositiveIntegerField(verbose_name='توان مصرفی')),
                ('boost_frequency', models.CharField(max_length=1000, verbose_name='فرکانس بوست')),
                ('architecture_size', models.CharField(max_length=1000, verbose_name='معماری اندازه')),
            ],
            bases=('product.productmodel',),
        ),
        migrations.CreateModel(
            name='FanCpuModel',
            fields=[
                ('productmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.productmodel')),
                ('weight', models.CharField(max_length=1000, verbose_name='وزن')),
                ('dimensions', models.CharField(max_length=1000, verbose_name='ابعاد')),
                ('radiator_material', models.CharField(max_length=1000, verbose_name='جنس رادیاتور')),
                ('fan_size', models.CharField(max_length=1000, verbose_name='سایز فن')),
                ('power_usage', models.CharField(max_length=1000, verbose_name='توان مصرفی')),
                ('tdp', models.PositiveIntegerField(verbose_name='توان tdp')),
            ],
            bases=('product.productmodel',),
        ),
        migrations.CreateModel(
            name='GpuModel',
            fields=[
                ('productmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.productmodel')),
                ('storage_bus', models.CharField(max_length=1000, verbose_name='باس حافظه')),
                ('core_frequency', models.CharField(max_length=10000, verbose_name='فرکانس هسته')),
                ('storage_frequency', models.CharField(max_length=1000, verbose_name='فرکانس حافظه')),
                ('power_usage', models.CharField(max_length=1000, verbose_name='نوان مصرفی')),
                ('suggested_power', models.CharField(max_length=1000, verbose_name='پاور پیشنهادی')),
                ('power_connectors', models.CharField(max_length=1000, verbose_name='کانکنور پاور')),
                ('Hdmi_port', models.PositiveIntegerField(verbose_name='پورت hdmi')),
                ('display_port', models.PositiveIntegerField(verbose_name='پورت display')),
                ('mini_display_port', models.PositiveIntegerField(verbose_name='پورت mini display')),
                ('dvi_port', models.PositiveIntegerField(verbose_name='پورت dvi')),
                ('vga_port', models.PositiveIntegerField(verbose_name='پورت vga')),
                ('type_c_port', models.PositiveIntegerField(verbose_name='پورت type c')),
                ('direct_x', models.CharField(max_length=1000, verbose_name='دایرکت x')),
                ('multi_gpu', models.BooleanField(verbose_name='مولتی گرافیک')),
                ('resolution', models.CharField(max_length=1000, verbose_name='رزولیشن')),
            ],
            bases=('product.productmodel',),
        ),
        migrations.CreateModel(
            name='HardModel',
            fields=[
                ('productmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.productmodel')),
                ('dimensions', models.CharField(max_length=1000, verbose_name='ابعاد')),
                ('head_size', models.CharField(max_length=1000, verbose_name='سایز هد')),
                ('storage', models.CharField(max_length=1000, verbose_name='حافظه')),
                ('cache', models.CharField(max_length=1000, verbose_name='کش')),
                ('rotor_speed', models.CharField(max_length=1000, verbose_name='سرعت روتور')),
                ('water_proof', models.BooleanField(verbose_name='ضد آب')),
                ('weight', models.CharField(max_length=1000, verbose_name='وزن')),
                ('noise_level', models.CharField(max_length=1000, verbose_name='سطح نویز')),
                ('power_usage', models.CharField(max_length=1000, verbose_name='توان مصرفی')),
                ('frequency_limit', models.CharField(max_length=1000, verbose_name='بازه فرکانس')),
            ],
            bases=('product.productmodel',),
        ),
        migrations.CreateModel(
            name='KeyBoardModel',
            fields=[
                ('productmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.productmodel')),
            ],
            bases=('product.productmodel',),
        ),
        migrations.CreateModel(
            name='LaptopModel',
            fields=[
                ('productmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.productmodel')),
                ('on_site_gpu', models.BooleanField(verbose_name='گرافیک مجزا')),
                ('weight', models.FloatField(verbose_name='وزن')),
                ('battery_storage', models.PositiveIntegerField(verbose_name='ظرفیت باتری')),
                ('power_adaptor', models.PositiveIntegerField(verbose_name='اداپتور پاور')),
            ],
            bases=('product.productmodel',),
        ),
        migrations.CreateModel(
            name='MainBoardModel',
            fields=[
                ('productmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.productmodel')),
                ('has_wifi', models.BooleanField(verbose_name='وای فای')),
                ('has_bluetooth', models.BooleanField(verbose_name='بلوتوث')),
                ('number_of_ram_slot', models.PositiveIntegerField(verbose_name='تعداد اسلات رم')),
                ('dimensions', models.CharField(max_length=1000, verbose_name='ابعاد')),
                ('has_hdmi_port', models.BooleanField(verbose_name='پورت hdmi')),
                ('has_vga_port', models.BooleanField(verbose_name='پورت vga')),
                ('has_display_port', models.BooleanField(verbose_name='پورت display')),
                ('voice_card', models.CharField(max_length=1000, verbose_name='کارت صدا')),
                ('usb_ports', models.CharField(max_length=1000, verbose_name='پورت usb')),
                ('lan_port', models.CharField(max_length=1000, verbose_name='پورت lan')),
                ('jack_3_5', models.CharField(max_length=1000, verbose_name='جک 3.5')),
                ('pci_slots', models.CharField(max_length=1000, verbose_name='اسلات pci')),
                ('power_connector', models.CharField(max_length=1000, verbose_name='کانکتور پاور')),
            ],
            bases=('product.productmodel',),
        ),
        migrations.CreateModel(
            name='MonitorModel',
            fields=[
                ('productmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.productmodel')),
            ],
            bases=('product.productmodel',),
        ),
        migrations.CreateModel(
            name='MouseModel',
            fields=[
                ('productmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.productmodel')),
            ],
            bases=('product.productmodel',),
        ),
        migrations.CreateModel(
            name='OpticalDriveModel',
            fields=[
                ('productmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.productmodel')),
            ],
            bases=('product.productmodel',),
        ),
        migrations.CreateModel(
            name='PowerModel',
            fields=[
                ('productmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.productmodel')),
                ('output_power', models.PositiveIntegerField(verbose_name='توان خروجی')),
                ('dimensions', models.CharField(max_length=1000, verbose_name='ابعاد')),
                ('weight', models.CharField(max_length=1000, verbose_name='وزن')),
                ('modular', models.BooleanField(verbose_name='ماژولار')),
                ('standard_certificate', models.CharField(max_length=1000, verbose_name='گواهینامه استاندارد')),
                ('limit_frequency', models.CharField(max_length=1000, verbose_name='محدوده فرکانس')),
                ('output_ports', models.CharField(max_length=1000, verbose_name='پورت های خروجی')),
            ],
            bases=('product.productmodel',),
        ),
        migrations.CreateModel(
            name='RamModel',
            fields=[
                ('productmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.productmodel')),
                ('number_of_module', models.PositiveIntegerField(verbose_name='تعداد ماژول ')),
                ('storage', models.CharField(max_length=1000, verbose_name='حافظه')),
                ('cl_number', models.CharField(max_length=1000, verbose_name='شماره cl')),
                ('number_of_pin', models.CharField(max_length=1000, verbose_name='تعداد پین')),
                ('timing', models.CharField(max_length=1000, verbose_name='تایمینگ')),
                ('number_of_channels', models.CharField(max_length=1000, verbose_name='تعداد کانال')),
                ('has_rgb', models.BooleanField(verbose_name='دارای rgb')),
            ],
            bases=('product.productmodel',),
        ),
        migrations.CreateModel(
            name='SpeakerModel',
            fields=[
                ('productmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.productmodel')),
            ],
            bases=('product.productmodel',),
        ),
        migrations.CreateModel(
            name='SSDModel',
            fields=[
                ('productmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.productmodel')),
                ('read_speed', models.CharField(max_length=1000, verbose_name='سرعت خوانندن')),
                ('write_speed', models.CharField(max_length=1000, verbose_name='سرعت نوشتن')),
                ('storage', models.CharField(max_length=1000, verbose_name='حافظه')),
                ('head_sing', models.BooleanField(verbose_name='هیدسینگ')),
            ],
            bases=('product.productmodel',),
        ),
        migrations.CreateModel(
            name='UserFavoriteProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_product', to='product.productmodel', verbose_name='کالا')),
            ],
        ),
    ]