# Generated by Django 4.2.1 on 2024-08-14 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0004_faqquestionmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitedetailmodel',
            name='work_time',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]