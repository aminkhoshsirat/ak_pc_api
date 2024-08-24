# Generated by Django 4.2.1 on 2024-08-08 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_initial'),
        ('notification', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotificationmodel',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='user_notification', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='adminnotificationmodel',
            name='blog_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='blog_comment_admin_notification', to='blog.blogcommentmodel'),
        ),
        migrations.AddField(
            model_name='adminnotificationmodel',
            name='product_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_comment_admin_notification', to='product.productcommentmodel'),
        ),
    ]
