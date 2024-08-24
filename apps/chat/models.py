from django.db import models
from apps.user.models import UserModel
from django_jalali.db import models as jmodels


class UserChatRoomModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.DO_NOTHING, related_name='user_chats')
    date = jmodels.jDateTimeField(auto_now=True)
    last_text = models.TextField(null=True, blank=True)
    admin = models.BooleanField(default=False)
    online = models.BooleanField(default=False)


class UserChatModel(models.Model):
    chat_room = models.ForeignKey(UserChatRoomModel, on_delete=models.DO_NOTHING, related_name='room_chats')
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, related_name='send_user', blank=True, null=True)
    replay = models.ForeignKey('UserChatModel', on_delete=models.DO_NOTHING, related_name='chat_replays', blank=True, null=True)
    text = models.TextField()
    date = jmodels.jDateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
