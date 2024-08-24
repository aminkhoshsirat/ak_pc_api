import json
import requests

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import FormMixin
from itertools import chain
from operator import attrgetter
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum
from apps.bucket.models import BucketProductsModel
from apps.product.models import ProductCommentModel, ProductModel
from apps.blog.models import BlogCommentModel
from apps.chat.models import UserChatRoomModel, UserChatModel
from apps.bucket.models import BuketModel
from django.utils import timezone
from apps.product.models import *
from .forms import *
from .models import *
from apps.product.serializers import ProductCommentSerializers
from apps.blog.serializers import BlogCommentSerializers
from apps.bucket.serializers import BucketProductSerializers
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.db.models.aggregates import Max
from django.db.models import F
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Sum
import datetime
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from utils.create_base_categories import create_categories
from apps.notification.models import AdminNotificationModel
from akurtekPC.config import ghasedak_api_key
from apps.user.forms import AddAdminForm, AddUserForm
from apps.blog.models import BlogCategoryModel, BlogCommentModel, BlogModel, AutherModel
from apps.blog.forms import AutherForm, BlogForm, BlogCategoryForm


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin


class SuperRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class AutherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_auther


class HeaderView(AdminRequiredMixin, View):
    def get(self, request):
        admin_notifications = AdminNotificationModel.objects.filter(admin_seen=False).order_by('-date')
        context = {
            'admin_notifications': admin_notifications,
        }
        return render(request, 'panel/partial/header.html', context)


class SideBarView(AdminRequiredMixin, View):
    def get(self, request):
        context = {
            'site_detail': SiteDetailModel.objects.first()
        }
        return render(request, 'panel/partial/sidebar.html', context)


class IndexView(AdminRequiredMixin, View):
    def get(self, request):
        recently_sell_products = BucketProductsModel.objects.filter(bucket__is_paid=True).order_by('-id')
        max_sell = ProductModel.objects.filter(sell__gt=0).aggregate(max=Max('sell'))
        most_sell_products = ProductModel.objects.filter(sell__gt=0).annotate(persent=(F('sell') * 100 / max_sell['max'])).order_by('-sell')[0:10]
        buckets = BuketModel.objects.filter(is_paid=True)
        users = UserModel.objects.filter(is_admin=False, is_superuser=False)
        order_paid = buckets.aggregate(total=Sum('price_paid'))

        try:
            order_user = int(order_paid.get('total') / users.count())
        except:
            order_user = 0

        # ghasedak
        try:
            url = "http://api.ghasedaksms.com/v2/credit"

            headers = {
                'apikey': "RjZN5VorYOuI01duQPGOT5cE+DfLh6PDwPyEKYDpDwI",
            }
            response = requests.request("POST", url, headers=headers)
            ghasedak_amount = int(json.loads(response.text)['credit'] / 10)

            ghasedak_amount = f'{ghasedak_amount:,}'
        except:
            ghasedak_amount = 0

        context = {
            'recently_sell_products': recently_sell_products,
            'most_sell_products': most_sell_products,
            'room_name': 'broadcast',
            'order_num': buckets.count,
            'order_paid': order_paid,
            'users_num': users.count,
            'order_user': order_user,
            'ghasedak_amount': ghasedak_amount,
        }
        return render(request, 'panel/index.html', context)


class ProductCategoryView(AdminRequiredMixin, View):

    def get(self, request):
        main_categories = MainCategoryModel.objects.prefetch_related('base_category_child').all()
        context = {
            'main_categories': main_categories,
            'main_category_form': MainCategoryForm,
            'child_category_form': ChildCategoryForm,
        }
        return render(request, 'panel/products-categories.html', context)

    def post(self, request):
        if 'base_category' in request.POST:
            form = ChildCategoryForm(request.POST, self.request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                child_category = ChildCategoryModel.objects.create(title=cd['title'], url=cd['url'],
                                                                   base_category=cd['base_category'],
                                                                   parent_category=cd['parent_category'],
                                                                   active=cd['active'])
                ChildCategoryImageModel.objects.create(child_category=child_category, image=cd['image'],
                                                       description=cd['description'])
                messages.add_message(request, messages.SUCCESS, 'دسته بندی اضافه شد')
                redirect('panel:products_category')
            else:
                redirect('panel:products_category')

        else:
            form = MainCategoryForm(request.POST, self.request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                main_category = MainCategoryModel.objects.create(title=cd['title'], url=cd['url'],
                                                                 active=cd['active'])
                MainCategoryImageModel.objects.create(main_category=main_category,
                                                      image=cd['image'], description=cd['description'])
                return redirect('panel:products_category')
            else:
                return redirect('panel:products_category')
        return redirect('panel:products_category')


class ProductListView(AdminRequiredMixin, ListView):
    model = ProductModel
    template_name = 'panel/products-list.html'
    paginate_by = 20
    context_object_name = 'products'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['main_category'] = MainCategoryModel.objects.prefetch_related('base_category_child')
        return context

    def get_queryset(self):
        category = self.request.GET.get('category')
        date = self.request.GET.get('date')
        status = self.request.GET.get('status')

        products = ProductModel.objects.all().order_by('-published_date')

        if category:
            products = products.filter(Q(main_category__url=category) | Q(child_category__url=category))

        if date:
            products = products.filter(published_date=date)

        if status:
            products = products.filter(status=status)

        return products


class ProductGridListView(AdminRequiredMixin, ListView):
    template_name = 'panel/products-grid.html'
    model = ProductModel
    context_object_name = 'products'
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        child_category = []
        for i in ChildCategoryModel.objects.filter(active=True):
            if i.child_category_products:
                child_category.append(i)

        context['child_categories'] = child_category
        return context


class ProductGridBodyView(AdminRequiredMixin, ListView):
    template_name = 'panel/products-grid-body.html'
    model = ProductModel
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        category_id = self.request.GET.get('category')
        grid_type = self.request.GET.get('type')
        search = self.request.GET.get('search')

        products = ProductModel.objects.all()

        try:
            category_id = int(category_id)
            if category_id < 0:
                category_id = 0
        except:
            category_id = 0

        if category_id == 0:
            pass

        else:
            child_category = get_object_or_404(ChildCategoryModel, id=category_id)
            products = products.filter(child_category=child_category)

        if grid_type == 'last':
            pass

        elif grid_type == 'most_viewed':
            products = products.order_by('-view_num')

        elif grid_type == 'cheap':
            products = products.order_by('price_after_off')

        elif grid_type == 'expensive':
            products = products.order_by('-price_after_off')

        elif grid_type == 'most_sell':
            products = products.order_by('most_sell')

        if search:
            products = products.annotate(similar=Greatest(
                TrigramSimilarity('title', search),
                TrigramSimilarity('url', search),
                TrigramSimilarity('main_category__title', search),
                TrigramSimilarity('child_category__title', search),
            )).filter(similar__gt=0.1).order_by('-similar')

        return products


class ProductDeleteView(AdminRequiredMixin, View):
    def get(self, request, id):
        product = ProductModel.objects.filter(id=id)
        if product.exists():
            product.delete()
            return HttpResponse('success')
        else:
            return HttpResponse('product not found')


class OrderView(AdminRequiredMixin, ListView):
    template_name = 'panel/orders.html'
    context_object_name = 'orders'
    model = BuketModel
    queryset = BuketModel.objects.filter(is_paid=True)
    paginate_by = 20


class OrderDetailView(AdminRequiredMixin, DetailView):
    template_name = 'panel/order-detail.html'
    model = BuketModel
    context_object_name = 'order'
    queryset = BuketModel.objects.prefetch_related('bucket_products').filter(is_paid=True)


class DailyWorksViews(AdminRequiredMixin, ListView):
    model = DailyWorksModel
    template_name = 'panel/app-to-do.html'
    context_object_name = 'daily_works'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = DailyWorksForm()
        return context

    def get_queryset(self):
        date = timezone.now()
        DailyWorksModel.objects.filter(date__gt=date).order_by('date')
        return DailyWorksViews

    def post(self, request):
        form = DailyWorksForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            DailyWorksModel.objects.create(user=cd['user'], title=cd['title'],
                                           description=cd['description'], date=cd['date'])


class CalendarView(AdminRequiredMixin, View):
    def get(self, request):
        return render(request, 'panel/app-fullcalender.html')


class OldDailyWorksViews(AdminRequiredMixin, ListView):
    model = DailyWorksModel
    template_name = 'panel/app-to-do.html'
    context_object_name = 'daily_works'

    def get_queryset(self):
        date = timezone.now()
        DailyWorksModel.objects.filter(date__lt=date).order_by('date')
        return DailyWorksViews


class SiteDetailView(AdminRequiredMixin, View):
    def get(self, request):
        site_detail = SiteDetailModel.objects.all()
        if site_detail.exists():
            data = site_detail.first()
            form = SiteDetailForm(instance=data)
        else:
            form = SiteDetailForm()

        return render(request, 'panel/site-detail.html', {'form': form})

    def post(self, request):
        site_detail = SiteDetailModel.objects.all()
        if site_detail.exists():
            data = site_detail.first()
            form = SiteDetailForm(request.POST, request.FILES, instance=data)
        else:
            form = SiteDetailForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

        return redirect('panel:site_detail')


class FinancialStatementsView(AdminRequiredMixin, ListView):
    template_name = 'panel/app-invoice.html'
    paginate_by = 20
    model = FinancialStatementModel
    queryset = FinancialStatementModel.objects.all()
    context_object_name = 'financial_statements'


class FinancialStatementSingleView(AdminRequiredMixin, DetailView):
    template_name = 'panel/app-invoice-single.html'
    model = FinancialStatementModel
    context_object_name = 'financial_statement'

    def get_queryset(self):
        id = self.kwargs.get('pk')
        financial_statement = FinancialStatementModel.objects.prefetch_related('financial_statement_objects').annotate(
            total_price=Sum('financial_statement_objects__price'),
            total_price_after_off=Sum('financial_statement_objects__price')).filter(pk=id)

        print(financial_statement)

        return financial_statement


class FactorPdfView(AdminRequiredMixin, View):
    def get(self, request, id):
        response = HttpResponse(content_type='application/pdf')
        response['content-Disposition'] = f"attachement;filename={id}" + str(datetime.datetime.now()) + ".pdf"
        template = get_template('panel/factor.html')
        context = {
            'financial_statement': get_object_or_404(FinancialStatementModel, id=id)
        }
        html = template.render(context)
        pisa.CreatePDF(html, dest=response)

        return response


class FaqView(AdminRequiredMixin, View):
    def get(self, request):
        faqs = FaqQuestionModel.objects.all()
        form = FaqQuestionForm()
        context = {
            'faqs': faqs,
            'form': form
        }
        return render(request, 'panel/faq.html', context)

    def post(self, request):
        form = FaqQuestionForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('panel:faq')


class UserListView(AdminRequiredMixin, ListView):
    template_name = 'panel/users.html'
    context_object_name = 'users'
    paginate_by = 20
    queryset = UserModel.objects.filter(is_admin=False, is_superuser=False, is_staff=False)


class AdminView(AdminRequiredMixin, ListView):
    template_name = 'panel/admins.html'
    context_object_name = 'admins'
    paginate_by = 20
    queryset = UserModel.objects.filter(Q(is_admin=True) | Q(is_superuser=True) | Q(is_staff=True))


class AddAdminView(SuperRequiredMixin, View):
    def get(self, request):
        form = AddAdminForm()
        return render(request, 'panel/add-admin.html', {'form': form})

    def post(self, request):
        form = AddAdminForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()

            return redirect('panel:admin')
        return redirect('panel:add_admin')


class AddUserView(AdminRequiredMixin, View):
    def get(self, request):
        form = AddUserForm()
        return render(request, 'panel/add-admin.html', {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('panel:users')
        return redirect('panel:add_user')


class BlogCategoryView(AdminRequiredMixin, View):
    def get(self, request):
        context = {

        }
        return render(request, '', context)


class BlogListView(AdminRequiredMixin, ListView):
    template_name = ''
    context_object_name = 'blogs'
    paginate_by = 20
    model = BlogModel
    queryset = BlogModel.objects.all()


class BlogAddView(AutherRequiredMixin, View):
    def get(self, request):
        context = {

        }
        return render(request, '', context)


class AutherListView(AdminRequiredMixin, ListView):
    template_name = 'panel/authors.html'
    context_object_name = 'authors'
    paginate_by = 20
    model = AutherModel
    queryset = AutherModel.objects.all()


class AddAutherView(SuperRequiredMixin, View):
    def get(self, request):
        context = {
            'form': AutherForm()
        }
        return render(request, 'panel/add-auther.html', context)

    def post(self, request):
        form = AutherForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.is_admin = True
            user.is_auther = True
            user.save()
            return redirect('panel:auther')
        return redirect('panel:add_auther')


class AddProductView(AdminRequiredMixin, View):
    def get(self, request):
        create_categories()
        main_categories = MainCategoryModel.objects.prefetch_related('base_category_child').filter(active=True)
        return render(request, 'panel/add-product.html', {'main_categories': main_categories})


class AddNewProductView(AdminRequiredMixin, View):
    def get(self, request):
        category = request.GET.get('category')
        if category == 'cpu':
            form = CpuForm()

        elif category == 'main-board':
            form = MainBoardForm()

        elif category == 'gpu':
            form = GpuForm()

        elif category == 'fan-cpu':
            form = FanCpuForm()

        elif category == 'ram':
            form = RamForm()

        elif category == 'hard':
            form = HardForm()

        elif category == 'ssd':
            form = SSDForm()

        elif category == 'power':
            form = PowerForm()

        elif category == 'case':
            form = CaseForm()

        else:
            form = ProductForm()

        context = {
            'form': form,
            'category_url': category
        }
        print(form)

        return render(request, 'panel/add-product-form.html', context)

    def post(self, request):
        rp = request.POST
        rf = request.FILES
        category = request.GET.get('category')

        if 'cpu_platform_add' in rp:
            form = CpuPlatformForm(rp)
            if form.is_valid():
                form.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif 'socket_add' in rp:
            form = SocketTypeForm(rp)
            if form.is_valid():
                form.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif 'ddr_add' in rp:
            form = DDrForm(rp)
            if form.is_valid():
                form.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif 'series_add' in rp:
            form = SeriesForm(rp)
            if form.is_valid():
                form.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif 'bit_add' in rp:
            form = BiteTypeForm(rp)
            if form.is_valid():
                form.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif 'core_add' in rp:
            form = CpuCoreForm(rp)
            if form.is_valid():
                form.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif 'on_board_gpu_add' in rp:
            form = OnBoardGpuForm(rp)
            if form.is_valid():
                form.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif 'main_board_form_factor_add' in rp:
            form = FormFactorForm(rp)
            if form.is_valid():
                form.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif 'chipset_add' in rp:
            form = MainBoardChipSetForm(rp)
            if form.is_valid():
                form.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif 'ram_frequency_add' in rp:
            form = RamFrequencyForm(rp)
            if form.is_valid():
                form.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif 'gpu_platform_add' in rp:
            form = GpuPlatformForm(rp)
            if form.is_valid():
                form.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif 'gpu_ddr_add' in rp:
            form = GpuDDrForm(rp)
            if form.is_valid():
                form.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif 'hard_type_add' in rp:
            form = HardTypeForm(rp)
            if form.is_valid():
                form.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif 'sata_add' in rp:
            form = SataTypeForm(rp)
            if form.is_valid():
                form.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif 'ssd_type_add' in rp:
            form = SSDTypeForm(rp)
            if form.is_valid():
                form.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif 'power_factor_add' in rp:
            form = PowerFormFactorForm(rp)
            if form.is_valid():
                form.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                return redirect(request.META['HTTP_REFERER'])

        if category == 'cpu':
            form = CpuForm(rp, rf)
            if form.is_valid():
                form.save()
            else:
                pass

        elif category == 'main_board':
            form = MainBoardForm(rp, rf)
            if form.is_valid():
                form.save()
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif category == 'gpu':
            form = GpuForm(rp, rf)
            if form.is_valid():
                form.save()
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif category == 'fan_cpu':
            form = FanCpuForm(rp, rf)
            if form.is_valid():
                form.save()
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif category == 'ram':
            form = RamForm(rp, rf)
            if form.is_valid():
                form.save()
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif category == 'hard':
            form = HardForm(rp, rf)
            if form.is_valid():
                form.save()
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif category == 'ssd':
            form = SSDForm(rp, rf)
            if form.is_valid():
                form.save()
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif category == 'power':
            form = PowerForm(rf, rp)
            if form.is_valid():
                form.save()
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif category == 'case':
            form = CaseForm(rp, rf)
            if form.is_valid():
                form.save()
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif category == 'keyboard':
            form = KeyBoardForm(rp)
            if form.is_valid():
                form.save()
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif category == 'mouse':
            form = MouseForm(rp)
            if form.is_valid():
                form.save()
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif category == 'monitor':
            form = MonitorForm(rp)
            if form.is_valid():
                form.save()
            else:
                return redirect(request.META['HTTP_REFERER'])

        elif category == 'optical_drive':
            form = OpticalDriveForm(rp)
            if form.is_valid():
                form.save()
            else:
                return redirect(request.META['HTTP_REFERER'])


class HeaderApiView(IsAdminUser, APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        comments = sorted(
            chain(ProductCommentSerializers(ProductCommentModel.objects.filter(admin_seen=False), many=True).data,
                  BlogCommentSerializers(BlogCommentModel.objects.filter(admin_seen=False), many=True).data))
        context = {
            'comments': comments,
            'comments_count': json.dumps(len(comments)),
        }
        return Response(context)


class IndexApiView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        recently_sell_products = BucketProductSerializers(BucketProductsModel.objects.filter(bucket__is_paid=True).order_by('-id'), many=True).data
        context = {
            'recently_sell_products': recently_sell_products,
        }
        return Response(context)


class ProductCategoryApiView(View):
    def get(self, request):
        main_categories = MainCategoryModel.objects.prefetch_related('base_category_child').all()
        context = {
            'main_categories': main_categories,
            'main_category_form': MainCategoryForm,
            'child_category_form': ChildCategoryForm,
        }
        return render(request, 'panel/products-categories.html', context)

    def post(self, request):
        if 'base_category' in request.POST:
            form = ChildCategoryForm(request.POST, self.request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                child_category = ChildCategoryModel.objects.create(title=cd['title'], url=cd['url'],
                                                                   base_category=cd['base_category'],
                                                                   parent_category=cd['parent_category'],
                                                                   active=cd['active'])
                ChildCategoryImageModel.objects.create(child_category=child_category, image=cd['image'],
                                                       description=cd['description'])
                messages.add_message(request, messages.SUCCESS, 'دسته بندی اضافه شد')
                redirect('panel:products_category')
            else:
                redirect('panel:products_category')

        else:
            form = MainCategoryForm(request.POST, self.request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                main_category = MainCategoryModel.objects.create(title=cd['title'], url=cd['url'],
                                                                 active=cd['active'])
                MainCategoryImageModel.objects.create(main_category=main_category,
                                                      image=cd['image'], description=cd['description'])
                return redirect('panel:products_category')
            else:
                return redirect('panel:products_category')
        return redirect('panel:products_category')
