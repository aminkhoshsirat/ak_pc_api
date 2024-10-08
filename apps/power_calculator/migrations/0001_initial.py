# Generated by Django 4.2.1 on 2024-08-08 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CpuBrandsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='DriveModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=1000)),
                ('power', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FanModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=500)),
                ('power', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='GpuBrandsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='HardModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=500)),
                ('power', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LiquidFanModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=500)),
                ('power', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MainBoardModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_factor', models.CharField(max_length=500)),
                ('power', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RamModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=500)),
                ('power', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SSDModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=500)),
                ('power', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='GpuSeriesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='gpu_series', to='power_calculator.gpubrandsmodel')),
            ],
        ),
        migrations.CreateModel(
            name='GpuModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('power', models.PositiveIntegerField()),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='series_gpu', to='power_calculator.gpuseriesmodel')),
            ],
        ),
        migrations.CreateModel(
            name='CpuSocketModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='brands_socket', to='power_calculator.cpubrandsmodel')),
            ],
        ),
        migrations.CreateModel(
            name='CpuModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('power', models.PositiveIntegerField()),
                ('socket', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='socket_cpus', to='power_calculator.cpusocketmodel')),
            ],
        ),
    ]
