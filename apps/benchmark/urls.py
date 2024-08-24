from django.urls import path
from .views import *

app_name = 'benchmark'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('cpu/<category>/<type>', CpuBenchmarkView.as_view(), name='cpu'),
    path('cpu/<url>', CpuSingleBenchmarkView.as_view(), name='single_cpu'),
    path('gpu/<category>', GpuBenchmarkView.as_view(), name='gpu'),
    path('gpu/<url>', GpuBenchmarkView.as_view(), name='single_gpu'),
    path('ram/<category>', RamBenchmarkView.as_view(), name='ram'),
    path('ram/<url>', RamBenchmarkView.as_view(), name='single_ram'),
    path('disk/<category>', DiskBenchmarkView.as_view(), name='disk'),
    path('disk/<url>', DiskBenchmarkView.as_view(), name='single_disk'),
    path('pc/<category>', PcBenchmarkView.as_view(), name='pc'),
    path('pc/<url>', PcBenchmarkView.as_view(), name='single_pc'),
]
