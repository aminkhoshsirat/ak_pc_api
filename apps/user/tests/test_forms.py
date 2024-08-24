from django.test import TestCase
from ..forms import *


class TestLoginForm(TestCase):

    def test_valid_data(self):
        form = UserLoginForm(data={'phone_or_email': '09355631524', 'password': '2256aaL222'})
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = UserLoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)


class TestRegisterForm(TestCase):

    def test_valid_data(self):
        form = UserRegisterForm(data={'phone': '09355631524', 'email': 'amin@gmail.com', 'password': '2256aaL222',
                                      'confirm_password': '2256aaL222'})
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = UserRegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_confirm_password(self):
        form = UserRegisterForm(data={'phone': '09355631524', 'email': 'amin@gmail.com', 'password': '2256aaL222',
                                      'confirm_password': '2256aaK222'})
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'confirm_password', 'پسورد و تکرار آن یکی نمی باشد')

    def test_stretcher_password(self):
        form = UserRegisterForm(data={'phone': '09355631524', 'email': 'amin@gmail.com', 'password': '225252525',
                                      'confirm_password': '225252525'})
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'confirm_password', 'پسورد باید شامل اعداد و حروف کوچک و بزرگ باشد و حداقل 8 کاراکتر.')


class TestEditForm(TestCase):
    def test_valid_data(self):
        form = UserEditForm(data={'fullname': 'amin', 'phone': '09355631524', 'email': 'amin@gmail.com', 'post_code': '1234567890', 'address': 'buhb'})
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = UserEditForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)