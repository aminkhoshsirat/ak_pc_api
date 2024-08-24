from django.urls import path
from .views import *

app_name = 'power'

urlpatterns = [
    path('', PowerApiView.as_view()),
    path('test', TestView.as_view()),
    path('socket/<title>', CpuSocketApiView.as_view()),
    path('cpus/<title>', CpusApiView.as_view()),
    path('gpu-series/<id>', GpuSeriesApiView.as_view()),
    path('gpus/<id>', GpusApiView.as_view()),
]