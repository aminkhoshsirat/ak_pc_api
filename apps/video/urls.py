from django.urls import path
from .views import *

app_name = 'video'

urlpatterns = [
    path('', VideoView.as_view(), name='index'),
]