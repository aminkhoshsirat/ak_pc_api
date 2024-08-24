from django.shortcuts import render, HttpResponse
from django.views.generic import View, ListView, DetailView
from apps.product.models import *
from apps.product.serializers import ProductSerializers
from apps.product.category_fields import product_fields
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView


class AsembleView(View):
    def get(self, request):
        return render(request, 'asemble/asemble_form.html')


class CategoryView(ListView):
    template_name = 'asemble/category.html'
    paginate_by = 20
    queryset = ProductModel.objects.all()
    context_object_name = 'products'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        category = self.request.GET.get('category')
        if category == 'cpu':
            platform = CpuPlatformModel.objects.all()
            socket = SocketTypeModel.objects.all()
            ddr = DDRModel.objects.all()
            series = SeriesModel.objects.all()
            bit = BitTypeModel.objects.all()
            gpu = OnBoardGpuModel.objects.all()
            field_list = [{'name': CpuPlatformModel._meta.verbose_name.title, 'fields': platform},
                    {'name': SocketTypeModel._meta.verbose_name.title, 'fields': socket},
                    {'name': DDRModel._meta.verbose_name.title, 'fields': ddr},
                    {'name': SeriesModel._meta.verbose_name.title, 'fields': series},
                    {'name': BitTypeModel._meta.verbose_name.title, 'fields': bit},
                    {'name': OnBoardGpuModel._meta.verbose_name.title, 'fields': gpu},
            ]
            context['field_list'] = field_list

        elif category == 'main_board':
            form_factor = FormFactorModel.objects.all()
            ddr = DDRModel.objects.all()
            chipset = MainBoardChipSetModel.objects.all()
            frequency = RamFrequencyModel.objects.all()
            bit = BitTypeModel.objects.all()
            gpu = OnBoardGpuModel.objects.all()
            field_list = [{'name': DDRModel._meta.verbose_name.title, 'fields': ddr},
                          {'name': FormFactorModel._meta.verbose_name.title, 'fields': form_factor},
                          {'name': MainBoardChipSetModel._meta.verbose_name.title, 'fields': chipset},
                          {'name': RamFrequencyModel._meta.verbose_name.title, 'fields': frequency},
                          {'name': BitTypeModel._meta.verbose_name.title, 'fields': bit},
                          {'name': OnBoardGpuModel._meta.verbose_name.title, 'fields': gpu},
                          ]
            context['field_list'] = field_list

        elif category == 'ram':
            frequency = RamFrequencyModel.objects.all()
            field_list = [{'name': RamFrequencyModel._meta.verbose_name.title, 'fields': frequency},
                          ]
            context['field_list'] = field_list

        elif category == 'gpu':
            platform = GpuPlatformModel.objects.all()
            ddr = GpuDDRModel.objects.all()
            field_list = [{'name': GpuDDRModel._meta.verbose_name.title, 'fields': ddr},
                          {'name': GpuPlatformModel._meta.verbose_name.title, 'fields': platform},
                          ]
            context['field_list'] = field_list

        return context

    def get_queryset(self):
        category = self.request.GET.get('category')
        products = ''

        if category == 'cpu':
            products = CpuModel.objects.filter(active=True)

        if category == 'main_board':
            cpu_id = self.request.GET.get('cpu-id')
            cpu = CpuModel.objects.get(id=cpu_id)
            products = MainBoardModel.objects.filter(socket=cpu.socket, active=True)

        elif category == 'ram':
            main_board_id = self.request.GET('main_board_id')
            main_board = MainBoardModel.objects.get(id=main_board_id)
            products = RamModel.objects.filter(ddr=main_board.ddr, active=True)

        elif category == 'gpu':
            products = GpuModel.objects.filter(active=True)

        elif category == 'hard':
            products = HardModel.objects.filter(active=True)

        elif category == 'ssd':
            products = SSDModel.objects.filter(active=True)

        elif category == 'drive':
            products = OpticalDriveModel.objects.filter(active=True)

        elif category == 'fan_cpu':
            cpu_id = self.request.GET('cpu_id')
            cpu = CpuModel.objects.get(id=cpu_id)
            products = FanCpuModel.objects.filter(tdp__gt=1.25 * cpu.tdp)

        elif category == 'case':
            products = CaseModel.objects.filter(active=True)

        elif category == 'monitor':
            products = MonitorModel.objects.filter(active=True)

        elif category == 'fan_case':
            pass

        elif category == 'power':
            products = PowerModel.objects.filter(active=True)

        return products


class ProductDetailView(DetailView):
    template_name = 'asemble/product-detail.html'
    context_object_name = 'product'
    queryset = ProductModel.objects.filter(active=True)
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['fields'] = product_fields(context['product'])
        return context



#--------------------------------------Api Views --------------------------------------------------

class ProductDetailApiView(ListAPIView):

    def get_serializer_context(self, **kwargs):
        context = super().get_context_data()
        context['fields'] = product_fields(context['product'])
        return context
