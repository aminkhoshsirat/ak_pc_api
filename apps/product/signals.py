from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProductCommentModel
from apps.notification.models import AdminNotificationModel
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(signal=post_save, sender=ProductCommentModel)
def create_admin_notification_for_product_comments(sender, instance, created, **kwargs):
    if created:
        comment = instance
        AdminNotificationModel.objects.create(title=f'یک کامنت محصول از طرف کاربر{comment.user.fullname} ',
                                              type='product_comment', product_comment=comment)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'comment_notification',
            {
                "type": "send_notification",
                "message": f'یک کامنت محصول از طرف کاربر{comment.user.fullname} '
            }
        )
