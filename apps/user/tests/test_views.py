from django.test import Client, TestCase
from django.shortcuts import reverse
from ..views import *


class TestUserLoginView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(phone='09909794694', fullname='amin', email='aminkhoshsirat1381@gmail.com', password='aminkh2565')

    def test_user_login_GET(self):
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')

    def test_user_login_POST_valid_password(self):
        response = self.client.post(reverse('user:login'), data={'phone_or_email': self.user.phone, 'password': 'aminkh2565'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_user_login_POST_invalid_password(self):
        pass
