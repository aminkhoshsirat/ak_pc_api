import json

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import UserChatModel
import urllib.parse as urlparse


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope['user']
        query = self.scope['query_string'].decode('utf-8')
        params = urlparse.parse_qs(query)
        print(self.scope['path'])
        replay = params.get('replay_id', [None])[0]

        replay_object = await UserChatModel.objects.filter(id=replay, chat_room_id=self.room_group_name).afirst()

        await UserChatModel.objects.acreate(chat_room_id=self.room_group_name, user=user,
                                            replay=replay_object, text=message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))