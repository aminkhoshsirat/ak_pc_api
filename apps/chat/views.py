from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import mark_safe
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework.generics import ListAPIView


class UserChatView(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user
        chat_room = UserChatRoomModel.objects.filter(user=user).first()
        if chat_room:
            chat_room.online = True
            context = {
                'chats': UserChatModel.objects.filter(chat_room=chat_room).order_by('-date')[::-1],
                'room_id': mark_safe(chat_room.id)
            }

        else:
            chat_room = UserChatRoomModel.objects.create(user=user, online=True)
            context = {
                'room_id': mark_safe(chat_room.id)
            }
        return render(request, 'chat/user-chat.html', context)


class AdminChatRoomView(ListView):
    template_name = 'panel/chat-box.html'
    model = UserChatRoomModel
    paginate_by = 20
    queryset = UserChatRoomModel.objects.all().order_by('-date')
    context_object_name = 'chat_rooms'


class AdminChatView(View):
    def get(self, request, id):
        chat_room = UserChatRoomModel.objects.filter(id=id).first()
        chats = UserChatModel.objects.filter(chat_room=chat_room).order_by('-date')[::-1]

        context = {
            'chat_room': chat_room,
            'chats': chats,
            'room_id': mark_safe(chat_room.id)
        }
        return render(request, 'panel/chat.html', context)


class UserChatApiView(LoginRequiredMixin, APIView):
    def get(self, request):
        user = self.request.user
        chat_room = UserChatRoomModel.objects.filter(user=user).first()
        if chat_room:
            chat_room.online = True
            data = {
                'chats':UserChatSerializers(UserChatModel.objects.filter(chat_room=chat_room).order_by('-date')[::-1], many=True),
                'room_id': mark_safe(chat_room.id)
            }

        else:
            chat_room = UserChatRoomModel.objects.create(user=user, online=True)
            data = {
                'room_id': mark_safe(chat_room.id)
            }

        return Response(data, status=status.HTTP_200_OK)


class AdminChatRoomApiView(ListAPIView):
    serializer_class = UserChatSerializers
    queryset = UserChatRoomModel.objects.all().order_by('-date')


class AdminChatApiView(APIView):
    def get(self, request, id):
        chat_room = UserChatRoomSerializers(UserChatRoomModel.objects.filter(id=id).first())
        chats = UserChatSerializers(UserChatModel.objects.filter(chat_room=chat_room).order_by('-date')[::-1])

        data = {
            'chat_room': chat_room,
            'chats': chats,
            'room_id': mark_safe(chat_room.id)
        }
        return Response(data, status=status.HTTP_200_OK)

