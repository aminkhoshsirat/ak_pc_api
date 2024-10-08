# Generated by Django 4.2.1 on 2024-08-20 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0006_contactusmodel_sitedetailmodel_about_us_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisingbannermodel',
            name='type',
            field=models.CharField(choices=[('desktop', 'desktop'), ('phone', 'phone')], default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='advertisingbannermodel',
            name='order',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=1000),
        ),
    ]
