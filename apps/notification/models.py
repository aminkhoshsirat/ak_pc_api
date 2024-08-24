from django.db import models
from apps.blog.models import BlogCommentModel
from apps.product.models import ProductCommentModel
from apps.user.models import UserModel
from django_jalali.db import models as jmodels


class TypeNotification(models.Choices):
    blog_comment = 'blog_comment'
    product_comment = 'product_comment'
    others = 'others'


class AdminNotificationModel(models.Model):
    title = models.CharField(max_length=10000)
    type = models.CharField(max_length=1000, choices=TypeNotification.choices)
    blog_comment = models.ForeignKey(BlogCommentModel, on_delete=models.DO_NOTHING,
                                     related_name='blog_comment_admin_notification', null=True, blank=True)
    product_comment = models.ForeignKey(ProductCommentModel, on_delete=models.DO_NOTHING,
                                        related_name='product_comment_admin_notification', null=True, blank=True)
    admin_description = models.TextField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    admin_seen = models.BooleanField(default=False)
    admin_seen_date = jmodels.jDateTimeField(null=True, blank=True)
    date = jmodels.jDateTimeField(auto_now_add=True)


class UserNotificationModel(models.Model):
    user = models.ManyToManyField(UserModel, related_name='user_notification', blank=True)
    title = models.CharField(max_length=10000)
    description = models.TextField()
    published_date = jmodels.jDateTimeField(auto_now_add=True)
    expire_date = jmodels.jDateTimeField()
