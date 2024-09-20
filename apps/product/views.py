import json
import redis
from django.db.models.aggregates import Count, Max, Min
from django.db.models.functions import Greatest
from django.contrib.postgres.search import TrigramSimilarity
from django.utils.timezone import now, datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from apps.blog.models import BlogCategoryModel, BlogModel
from apps.panel.models import SiteDetailModel, SuggestedProductsModel
from apps.panel.models import AmazingOfferModel, AdvertisingBannerModel, InstantOfferModel, FaqQuestionModel
from apps.panel.serializers import SiteDetailSerializer, InstantOfferSerializers, AdvertisingBannerSerializers, ContractUsSerializers
from apps.blog.serializers import BlogCategorySerializers, BlogSerializers
from apps.panel.serializers import FaqSerializers, AmazingOfferSerializers, SuggestedProductSerializers
from utils.services import get_client_ip
from .serializers import *
from .utils import *
from .category_fields import product_fields
from .forms import *
from rest_framework_tracking.mixins import LoggingMixin

r = redis.Redis(host='localhost', port=6379, db=0)


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20
    page_query_param = 'page'


class HeaderApiView(APIView):

    def get(self, request):
        main_categories = MainCategoryModel.objects.prefetch_related('base_category_child', 'main_category_image').filter(active=True)
        blog_categories = BlogCategoryModel.objects.prefetch_related('child').filter(active=True, parent=None)
        site_detail = SiteDetailModel.objects.first()
        data = {
            'main_categories': MainCategorySerializers(main_categories, many=True).data,
            'blog_categories': BlogCategorySerializers(blog_categories, many=True).data,
            'site_detail': SiteDetailSerializer(site_detail).data,
        }
        return Response(data, status=status.HTTP_200_OK)


class FooterApiView(APIView):
    def get(self, request):
        site_detail = SiteDetailModel.objects.first()
        data = {
            'site_detail': SiteDetailSerializer(site_detail).data,
        }
        return Response(data, status=status.HTTP_200_OK)


class FaqApiView(APIView):
    def get(self, request):
        questions = FaqQuestionModel.objects.all()
        data = {
            'questions': FaqSerializers(questions, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)


class ContactUsApiView(APIView):
    def get(self, request):
        site_detail = SiteDetailSerializer(SiteDetailModel.objects.first()).data
        return Response(site_detail, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ContractUsSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Success')

        else:
            return Response('Failed')


class ProductListApiView(APIView):
    pagination_class = CustomPagination

    @property
    def paginator(self):
        """The paginator instance associated with the view, or `None`."""
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """Return a single page of results, or `None` if pagination is disabled."""
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """Return a paginated style `Response` object for the given output data."""
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get(self, request):
        main_category_url = self.kwargs.get('main_category')
        child_category_url = self.kwargs.get('child_category')
        search = self.request.GET.get('search')
        sort = self.request.GET.get('sort')

        data = {}

        filter_dict = self.request.GET

        products = ProductModel.objects.filter(active=True)

        new_filter_dict = {}

        for i in filter_dict:
            if i != 'sort' and i != 'search':
                new_filter_dict[f'{i}__in'] = filter_dict.getlist(i)

        if main_category_url:
            main_category = MainCategoryModel.objects.prefetch_related('base_category_child').filter(
                url=main_category_url, active=True).first()
            data['main_category'] = MainCategorySerializers(main_category).data
            products = products.filter(main_category=main_category)

        elif child_category_url:
            child_category = ChildCategoryModel.objects.filter(url=child_category_url, active=True).first()
            data['child_category'] = ChildCategorySerializers(child_category).data
            products = products.filter(child_category=child_category)

        else:
            products = products.filter(active=True)

        if new_filter_dict:
            try:
                products = CpuModel.objects.filter(**new_filter_dict)
            except:
                pass

        if search:
            products = products.objects.annotate(similar=Greatest(
                TrigramSimilarity('title', search),
                TrigramSimilarity('url', search),
                TrigramSimilarity('main_category__title', search),
                TrigramSimilarity('child_category__title', search),
            )).filter(similar__gt=0.1).order_by('-similar')

        if sort:
            if sort == '1':
                products = products

            if sort == '2':
                products = products.annotate(count=Count('favorite_product')).order_by('-count')

            elif sort == '3':
                products = products.order_by('-sell')

            elif sort == '4':
                products = products.order_by('-published_date')

            elif sort == '5':
                products = products.order_by('price_after_off')

            elif sort == '6':
                products = products.order_by('-price_after_off')

        data['count_products'] = json.dumps(products.count())
        data['products_price'] = json.dumps(products.aggregate(max=Max('price_after_off'),
                                                               min=Min('price_after_off')))
        data['filters'] = json.dumps(filter_category(child_category_url))

        # pagination
        queryset = products
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductSerializers(page, many=True)
            data['products'] = serializer.data
            return self.get_paginated_response(data)

        pg_products = ProductSerializers(queryset, many=True)

        data['products'] = pg_products.data

        return Response(data, status.HTTP_200_OK)


class ProductDetailApiView(APIView):
    def get(self, request, slug):
        data = {

        }
        try:
            product = ProductModel.objects.get(url=slug)
            data['product'] = ProductSerializers(product).data
            amazing_offer = AmazingOfferModel.objects.filter(product=product, active=True).first()
            data['amazing_offer'] = AmazingOfferSerializers(amazing_offer).data
            data['images'] = ProductImageSerializers(ProductImageModel.objects.filter(product=product), many=True).data
            data['favorite_product'] = UserFavoriteProductModel.objects.filter(user_id=self.request.user.id,
                                                                               product=product).exists()

            data['fields'] = product_fields(product)

            ip = get_client_ip(self.request)

            user = self.request.user

            if user.is_authenticated:
                product_view, status = ProductViewModel.objects.get_or_create(product=product, ip=ip, user=user)

            else:
                product_view, status = ProductViewModel.objects.get_or_create(product=product, ip=ip)

            if status:
                product.view_num += 1
                product.save()

            try:
                data['product_in_bucket'] = json.loads(r.hget(
                    f'bucket:user:{self.request.user.phone}:product:{product.id}', 'num'))
            except:
                data['product_in_bucket'] = None
        except:
            pass

        return Response(data)


class ProductCommentView(ListAPIView): # -----------------------------------------------------------------------------------------------------------------
    template_name = 'product/comments.html'
    model = ProductCommentModel

    # def get_context_data(self, *args, **kwargs):
    #     context = super(*args, **kwargs)
    #     context['comment_average_grade'] = ProductCommentModel.objects.aggregate(Avg('grade'))
    #     return context

    # def get_queryset(self):
    #     product_id = self.kwargs.get('product_id')
    #     comments = ProductCommentModel.objects.prefetch_related('comment_positive_points', 'comment_negative_points').filter(product_id=product_id, active=True, admin_seen=True)
    #     print(comments)
    #     return comments
    #
    #
    # def post(self, request):
    #     form = ProductCommentForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #     else:
    #         return render(request, 'product/comments.html')


class ProductLikeApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        like_status = self.request.GET.get('like-status')
        if like_status == 'like':
            UserFavoriteProductModel.objects.get_or_create(user=request.user, product_id=id)
            return Response('like success')
        elif like_status == 'dislike':
            product = UserFavoriteProductModel.objects.filter(user=request.user, product_id=id)
            if product:
                product.delete()
                return Response('dislike success')
        return Response('error')


class ProductAddApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        user = request.user
        r.hset(f'bucket:user:{user.phone}:product:{id}', mapping={'product': id, 'num': 1})
        return Response('success')


class ProductDeleteApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        user = request.user
        r.delete(f'bucket:user:{user.phone}:product:{id}')
        return Response('success')


class ProductChangeApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        num = request.GET.get('num')
        try:
            num = int(num)
        except:
            num = 1
        if num < 1:
            num = 1
        user = request.user
        r.hset(f'bucket:user:{user.phone}:product:{id}', mapping={'product': id, 'num': num})
        return Response('success')


class ShowProductApiView(APIView):
    def get(self, request, id):
        try:
            product = ProductModel.objects.get(id=id)
            data = {
                'product': ProductSerializers(product).data,
                'images': ProductImageSerializers(ProductImageModel.objects.filter(product=product), many=True).data,
                'fields': product_fields(product),
            }
        except:
            data = {}
        return Response(data, status=status.HTTP_200_OK)


class ProductChartApiView(APIView):
    def get(self, request, id):
        products = ProductPriceChartModel.objects.filter(product_id=id)
        x = []
        y = []
        for i in products:
            x.append(i.date.strftime("%Y-%m-%d"))
            y.append(i.price)
        data = {
            'x_position': x,
            'y_position': y,
        }
        return Response(data, status=status.HTTP_200_OK)


class IndexApiView(LoggingMixin, APIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializers
    def get(self, request):
        products = ProductModel.objects.filter(active=True)
        categories = MainCategoryModel.objects.filter(active=True)
        brands = BrandModel.objects.filter(active=True)
        amazing_offers = AmazingOfferModel.objects.filter(active=True, expired_date__gt=now())
        instant_offers = InstantOfferModel.objects.filter(active=True, expired_date__gt=now())
        advertising_banners = AdvertisingBannerModel.objects.filter(active=True)
        blogs = BlogModel.objects.select_related('category').prefetch_related('auther').filter(active=True)[0:10]
        best_selling_products = products.order_by('-sell')[0:20]
        best_off_products = products.order_by('-off')[0:20]
        top_rating = products.order_by('-view_num')
        new_products = products.filter(available=True).order_by('-published_date')[0:20]
        amazing_offers = [{'product': ProductSerializers(i.product).data, 'fields': product_fields(i.product), 'date': i.expired_date} for i in amazing_offers]
        suggested_products = SuggestedProductsModel.objects.filter(active=True)
        max_off_suggested_products = suggested_products.aggregate(max_off=Max('product__off'))
        site_detail = SiteDetailModel.objects.all().first()
        assembled_cases = AssembledCaseModel.objects.filter(active=True)
        laptops = LaptopModel.objects.filter(active=True)
        cpus = CpuModel.objects.filter(active=True)
        main_boards = MainBoardModel.objects.filter(active=True)
        gpus = GpuModel.objects.filter(active=True)
        all_in_ones = AllInOneModel.objects.filter(active=True)
        data = {
            'categories': MainCategorySerializers(categories, many=True).data,
            'brands': BrandSerializers(brands, many=True).data,
            'blogs': BlogSerializers(blogs, many=True).data,
            'top_rating': ProductSerializers(top_rating, many=True).data,
            'best_selling_products': ProductSerializers(best_selling_products, many=True).data,
            'best_off_products': ProductSerializers(best_off_products, many=True).data,
            'new_products': ProductSerializers(new_products, many=True).data,
            'amazing_offers': amazing_offers,
            'instant_offers': InstantOfferSerializers(instant_offers, many=True).data,
            'suggested_products': SuggestedProductSerializers(suggested_products, many=True).data,
            'max_off_suggested_products': max_off_suggested_products,
            'site_detail': SiteDetailSerializer(site_detail).data,
            'advertising_banner1': AdvertisingBannerSerializers(advertising_banners.filter(order=1, type='desktop').first()).data,
            'advertising_banner2': AdvertisingBannerSerializers(advertising_banners.filter(order=2, type='desktop').first()).data,
            'advertising_banner3': AdvertisingBannerSerializers(advertising_banners.filter(order=3, type='desktop').first()).data,
            'advertising_banner4': AdvertisingBannerSerializers(advertising_banners.filter(order=4, type='desktop').first()).data,
            'advertising_banner5': AdvertisingBannerSerializers(advertising_banners.filter(order=1, type='phone').first()).data,
            'advertising_banner6': AdvertisingBannerSerializers(advertising_banners.filter(order=2, type='phone').first()).data,
            'advertising_banner7': AdvertisingBannerSerializers(advertising_banners.filter(order=3, type='phone').first()).data,
            'advertising_banner8': AdvertisingBannerSerializers(advertising_banners.filter(order=4, type='phone').first()).data,
            'assembled_cases': AssemblerSerializers(assembled_cases, many=True).data,
            'laptops': LaptopSerializers(laptops, many=True).data,
            'cpus': CpuSerializers(cpus, many=True).data,
            'main_boards': MainBoardSerializers(main_boards, many=True).data,
            'gpus': GpuSerializers(gpus, many=True).data,
            'all_in_ones': AllInOneSerializers(all_in_ones, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)


class CompareProductApiView(APIView):
    def get(self, request, category):
        id = self.request.GET.get('id')
        cp = compare_products(category, id)
        data = {
            'product': ProductSerializers(cp[0], many=True).data,
            'fields': cp[1],
        }
        return Response(data=data, status=status.HTTP_200_OK)


class CompareProductListApiView(ListAPIView):
    serializer_class = ProductSerializers

    def get_queryset(self):
        category = self.kwargs.get('category')
        search = self.request.GET.get('search')
        products = ProductModel.objects.filter(child_category__url=category, active=True)
        if search:
            products = products.annotate(similar=Greatest(
                TrigramSimilarity('title', search),
                TrigramSimilarity('url', search),
                TrigramSimilarity('main_category__title', search),
                TrigramSimilarity('child_category__title', search),
            )).filter(similar__gt=0.1).order_by('-similar')
        return products


