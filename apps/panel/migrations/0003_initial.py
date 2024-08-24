# Generated by Django 4.2.1 on 2024-08-08 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('panel', '0002_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyworksmodel',
            name='user',
            field=models.ManyToManyField(related_name='user_daily_works', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='amazingoffermodel',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='product_amazing_offer', to='product.productmodel'),
        ),
    ]
