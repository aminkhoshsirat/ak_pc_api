from django.test import TestCase
from ..models import *


class TestUserModel(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(phone='09909794694', fullname='amin', email='amin@gmail.com',
                                                  password='amin')

    def test_model_str(self):
        self.assertEqual(str(self.user), '09909794694 - amin')


class TestAddressModel(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(phone='09909794694', fullname='amin', email='amin@gmail.com',
                                                  password='amin')
        self.address = UserAddress.objects.create(user=self.user, state='azarbayjan', city='urmia', address='shahrak shahed',
                                                  plaque=10, post_code='1234567890')

    def test_model_str(self):
        self.assertEqual(str(self.address), '09909794694 - amin - shahrak shahed')