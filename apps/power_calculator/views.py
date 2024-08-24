import json
from django.views import View
from django.shortcuts import render
from rest_framework import status
from redis import Redis
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response

re = Redis(host='localhost', port=6379, db=0)

class TestView(View):
    def get(self, request):
        return render(request, 'test.html')


class PowerApiView(APIView):
    def get(self, request):
        gpu_brands = GpuBrandsModel.objects.all()

        main_boards = MainBoardModel.objects.all()

        rams = RamModel.objects.all()

        drives = DriveModel.objects.all()

        ssds = SSDModel.objects.all()

        hards = HardModel.objects.all()

        fans = FanModel.objects.all()

        liquid_fans = LiquidFanModel.objects.all()

        class Cpu:
            def __init__(self, li):
                self.li = li

        context = {
            'cpu_brands': ['Intel', 'AMD'],
            'gpu_brands': GpuBrandSerializer(gpu_brands, many=True).data,
            'main_boards': MainBoardSerializer(main_boards, many=True).data,
            'rams': RamSerializer(rams, many=True).data,
            'drives': DriverSerializer(drives, many=True).data,
            'ssds': SSDSerializer(ssds, many=True).data,
            'hards': HardSerializer(hards, many=True).data,
            'fans': FanSerializer(fans, many=True).data,
            'liquid_fans': LiquidSerializer(liquid_fans, many=True).data,
        }

        return Response(context, status=status.HTTP_200_OK)


class CpuSocketApiView(APIView):
    def get(self, request, title):
        if title == 'Intel':
            objects = re.get('intel_socket')
        else:
            objects = re.get('amd_socket')
        objects = json.loads(objects)
        return Response(objects, status=status.HTTP_200_OK)


class CpusApiView(APIView):
    def get(self, request, title):
        cpus = json.loads(re.get('cpus'))
        objects = []
        for i in cpus:
            if i['socket'].replace("Socket", "").lstrip(" ") == title:
                objects.append(i)
        return Response(objects, status=status.HTTP_200_OK)


class GpuSeriesApiView(APIView):
    def get(self, request, id):
        series = GpuSeriesModel.objects.filter(brand__id=id)
        data = {
            'objects': GpuSeriesSerializer(series, many=True).data
        }
        return Response(data=data, status=status.HTTP_200_OK)


class GpusApiView(APIView):
    def get(self, request, id):
        gpus = GpuModel.objects.filter(series_id=id)
        data = {
            'objects': GpuSerializer(gpus, many=True).data
        }
        return Response(data, status=status.HTTP_200_OK)
