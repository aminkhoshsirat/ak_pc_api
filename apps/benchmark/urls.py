from django.urls import path
from .views import *

app_name = 'benchmark'


urlpatterns = [
    path('', IndexApiView.as_view(), name='index'),
    path('cpu/<category>/<type>', CpuBenchmarkApiView.as_view(), name='cpu'),
    path('cpu/<url>', CpuSingleBenchmarkApiView.as_view(), name='single_cpu'),
    path('gpu/<category>', GpuBenchmarkApiView.as_view(), name='gpu'),
    path('gpu/<url>', GpuSingleBenchmarkApiView.as_view(), name='single_gpu'),
    path('ram/<category>', RamBenchmarkApiView.as_view(), name='ram'),
    path('ram/<url>', RamSingleBenchmarkApiView.as_view(), name='single_ram'),
    path('disk/<category>', DiskBenchmarkApiView.as_view(), name='disk'),
    path('disk/<url>', DiskSingleBenchmarkApiView.as_view(), name='single_disk'),
    path('pc/<category>', PcBenchmarkApiView.as_view(), name='pc'),
]
