import requests
from bs4 import BeautifulSoup
import redis
import json
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
try:
    schedule, _ = CrontabSchedule.objects.get_or_create(minute='51', hour='17', day_of_week='*', day_of_month='*',
                                                        month_of_year='*', timezone='Asia/Tehran'
                                                        )

    PeriodicTask.objects.get_or_create(crontab=schedule, name='cpu-benchmark-task',
                                       task='apps.benchmark.tasks.cpu_scrapy_tasks')

    PeriodicTask.objects.get_or_create(crontab=schedule, name='gpu-benchmark-task',
                                       task='apps.benchmark.tasks.gpu_scrapy_tasks')

    PeriodicTask.objects.get_or_create(crontab=schedule, name='ram-benchmark-task',
                                       task='apps.benchmark.tasks.ram_scrapy_tasks')

    PeriodicTask.objects.get_or_create(crontab=schedule, name='disk-benchmark-task',
                                       task='apps.benchmark.tasks.disk_scrapy_tasks')

    PeriodicTask.objects.get_or_create(crontab=schedule, name='pc-benchmark-task',
                                       task='apps.benchmark.tasks.pc_scrapy_tasks')
except:
    pass


r = redis.Redis(host='localhost', port=6379, db=0)


class IndexApiView(APIView):
    def get(self, request):
        details = json.loads(r.get(f'benchmark:pc:fastest-server'))
        categories = [
            {'title': 'پلتفرم', 'child': ['همه', 'کامپیوتر', 'لپتاپ']},
            {'title': 'گیمینگ', 'child': ['همه', 'کامپیوتر', 'لپتاپ']},
            {'title': 'اورکلاک', 'child': []},
            {'title': 'تک هسته', 'child': []},
        ]
        data = {
            'details': details,
            'categories': categories,
        }
        return Response(data, status.HTTP_200_OK)


class CpuBenchmarkApiView(APIView):
    def get(self, request, category, type):
        once = False
        categories = [
            {'title': 'پلتفرم', 'child': ['همه', 'کامپیوتر', 'لپتاپ']},
            {'title': 'گیمینگ', 'child': ['همه', 'کامپیوتر', 'لپتاپ']},
            {'title': 'اورکلاک', 'child': []},
            {'title': 'تک هسته', 'child': []},
        ]
        if category in ['overclock', 'single-thread']:
            once = True
        try:
            if once:
                details = json.loads(r.get(f'benchmark:cpu:{category}:once'))

            else:
                details = json.loads(r.get(f'benchmark:cpu:{category}:{type}'))
        except:
            details = None

        data = {
            'details': details,
            'categories': categories
        }

        return Response(data, status.HTTP_200_OK)


class CpuSingleBenchmarkApiView(APIView):
    def get(self, request, url):
        try:
            text = requests.get(f'https://www.cpubenchmark.net/cpu.php?{url}').text
            soup = BeautifulSoup(text, 'html.parser').find('div', class_='desc-body')
            details = []
            soup.find('div', class_='desc-body')
            for i in soup.find_all('p'):
                text = i.get_text().split(':')
                details.append({'name': text[0], 'amount': text[1:]})
        except:
            details = None
        return Response(details, status.HTTP_200_OK)


class GpuBenchmarkApiView(APIView):
    def get(self, request, category):
        categories = [
            {'title': 'g3d'},
            {'title': 'عملکرد بر اساس قیمت'},
            {'title': 'عملکرد مستقیم'},
            {'title': 'میان رده به بالا'},
            {'title': 'میان رده به پایین'},
            {'title': 'رده پایین'},
            {'title': 'رایج'},
        ]
        try:
            details = json.loads(r.get(f'benchmark:gpu:{category}'))
        except:
            details = None

        data = {
            'details': details,
            'categories': categories
        }

        return Response(data, status.HTTP_200_OK)


class GpuSingleBenchmarkApiView(APIView):
    def get(self, request, url):
        try:
            text = requests.get(f'https://www.videocardbenchmark.net/video_lookup.php?{url}').text
            soup = BeautifulSoup(text, 'html.parser').find('div', class_='desc-body')
            details = []
            soup.find('div', class_='desc-body')
            for i in soup.find_all('p'):
                text = i.get_text().split(':')
                details.append({'name': text[0], 'amount': text[1:]})
        except:
            details = None
        return Response(details)


class RamBenchmarkApiView(APIView):
    def get(self, request, category):
        categories = [
            {'title': 'DDR 5', 'child': {'همه', 'نوشتن', 'خواندن', 'تاخیر حافظه'}},
            {'title': 'DDR 4', 'child': ['همه', 'نوشتن', 'خواندن', 'تاخیر حافظه']},
            {'title': 'DDR 3', 'child': ['همه', 'نوشتن', 'خواندن', 'تاخیر حافظه']},
            {'title': 'DDR 2', 'child': ['همه', 'نوشتن', 'خواندن', 'تاخیر حافظه']},
        ]
        try:
            details = json.loads(r.get(f'benchmark:ram:{category}'))
        except:
            details = None
        data = {
            'details': details,
            'categories': categories
        }
        return Response(data, status.HTTP_200_OK)


class RamSingleBenchmarkApiView(APIView):
    def get(self, request, url):
        try:
            text = requests.get(f'https://www.memorybenchmark.net/ram.php?{url}').text
            soup = BeautifulSoup(text, 'html.parser').find('div', class_='desc-body')
            details = []
            soup.find('div', class_='desc-body')
            for i in soup.find_all('p'):
                text = i.get_text().split(':')
                details.append({'name': text[0], 'amount': text[1:]})
        except:
            details = None
        return Response(details, status.HTTP_200_OK)


class DiskBenchmarkApiView(APIView):
    def get(self, request, category):
        categories = [
            {'title': 'SSD', 'url': 'ssd'},
            {'title': 'رده بالا', 'url': 'disk-high'},
            {'title': 'میان رده به بالا', 'url': 'disk-high-mid-range'},
            {'title': 'میان رده به پایین', 'url': 'disk-low-mid-range'},
            {'title': 'رده پایین', 'url': 'disk-low-end'},
            {'title': 'خواندن متوالی ', 'url': 'sequential-read'},
            {'title': 'نوشتن متوالی', 'url': 'sequential-write'},
            {'title': 'نوشتن و خواندن رندوم', 'url': 'random-seek-read-write'},
            {'title': 'رایج', 'url': 'common'},
        ]
        try:
            details = json.loads(r.get(f'benchmark:disk:{category}'))
        except:
            details = None

        data = {
            'details': details,
            'categories': categories
        }

        return Response(data, status.HTTP_200_OK)


class DiskSingleBenchmarkApiView(APIView):
    def get(self, request, url):
        try:
            text = requests.get(f'https://www.harddrivebenchmark.net/hdd_lookup.php?{url}').text
            soup = BeautifulSoup(text, 'html.parser').find('div', class_='desc-body')
            details = []
            soup.find('div', class_='desc-body')
            for i in soup.find_all('p'):
                text = i.get_text().split(':')
                details.append({'name': text[0], 'amount': text[1:]})
        except:
            details = None
        return Response(details, status.HTTP_200_OK)


class PcBenchmarkApiView(APIView):
    def get(self, request, category):
        categories = [
            {'title': 'دسکتاپ', 'url': 'fastest-desktops'},
            {'title': 'سیستم', 'url': 'fastest-systems'},
            {'title': 'لپتاپ', 'url': 'fastest-laptops'},
            {'title': 'سرور', 'url': 'fastest-server'},
        ]
        try:
            details = json.loads(r.get(f'benchmark:pc:{category}'))
        except:
            details = None
        data = {
            'details': details,
            'categories': categories
        }
        return Response(data, status.HTTP_200_OK)
