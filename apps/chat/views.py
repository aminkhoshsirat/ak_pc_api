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
from rest_framework.permissions import IsAuthenticated


class UserChatApiView(LoginRequiredMixin, APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = self.request.user
        chat_room = UserChatRoomModel.objects.filter(user=user).first()
        if chat_room:
            chat_room.online = True
            data = {
                'chats': UserChatSerializers(UserChatModel.objects.filter(chat_room=chat_room).order_by('-date')[::-1],
                                             many=True).data,
                'room_id': chat_room.id
            }

        else:
            chat_room = UserChatRoomModel.objects.create(user=user, online=True)
            data = {
                'room_id': chat_room.id
            }

        return Response(data, status=status.HTTP_200_OK)


class AdminChatRoomApiView(ListAPIView):
    serializer_class = UserChatSerializers
    queryset = UserChatRoomModel.objects.all().order_by('-date')


class AdminChatApiView(APIView):
    def get(self, request, id):
        chat_room = UserChatRoomModel.objects.filter(id=id).first()
        chats = UserChatSerializers(UserChatModel.objects.filter(chat_room=chat_room).order_by('-date')[::-1],
                                    many=True).data

        data = {
            'chat_room': UserChatRoomSerializers(chat_room).data,
            'chats': chats,
            'room_id': chat_room.id
        }
        return Response(data, status=status.HTTP_200_OK)

