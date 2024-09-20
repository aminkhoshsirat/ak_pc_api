import json
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from apps.product.models import *
from apps.panel.models import *
from model_bakery import baker
from apps.blog.models import *
from django.utils.timezone import now, timedelta


class TestIndexView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        baker.make(MainCategoryModel, active=True)
        baker.make(ProductModel, active=True)
        baker.make(BrandModel, active=True)
        baker.make(AmazingOfferModel, active=True, expired_date=now() + timedelta(days=1))
        baker.make(InstantOfferModel, active=True, expired_date=now() + timedelta(days=1))
        baker.make(AdvertisingBannerModel, active=True)
        baker.make(BlogModel, active=True, text='test')
        baker.make(SuggestedProductsModel, active=True)
        baker.make(SiteDetailModel)
        baker.make(AssembledCaseModel, active=True)
        baker.make(LaptopModel, active=True)
        baker.make(CpuModel, active=True)
        baker.make(MainBoardModel, active=True)
        baker.make(GpuModel, active=True)
        baker.make(AllInOneModel, active=True)

    def test_index_view_GET(self):
        url = reverse('index')
        response = self.client.get(url)
        data = response.data
        self.assertTrue(response.status_code, 200)
        self.assertTrue(data.get('categories'))
        self.assertTrue(data.get('brands'))
        self.assertTrue(data.get('blogs'))
        self.assertTrue(data.get('top_rating'))
        self.assertTrue(data.get('best_selling_products'))
        self.assertTrue(data.get('best_off_products'))
        self.assertTrue(data.get('new_products'))
        self.assertTrue(data.get('amazing_offers'))
        self.assertTrue(data.get('instant_offers'))
        self.assertTrue(data.get('suggested_products'))
        self.assertTrue(data.get('max_off_suggested_products'))
        self.assertTrue(data.get('site_detail'))
        self.assertTrue(data.get('assembled_cases'))
        self.assertTrue(data.get('laptops'))
        self.assertTrue(data.get('cpus'))
        self.assertTrue(data.get('main_boards'))
        self.assertTrue(data.get('gpus'))
        self.assertTrue(data.get('all_in_ones'))


class TestConcatUsView(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_contact_us_GET(self):
        url = reverse('contact_us')
        response = self.client.get(url)
        print(response.data.values())
        self.assertTrue(response.data.values())
        self.assertTrue(response.status_code, 200)
