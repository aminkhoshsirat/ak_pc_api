import random
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django_jalali.db import models as jmodels
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import MinLengthValidator
from io import BytesIO
from PIL import Image


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, phone, email, fullname, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not phone:
            raise ValueError(_("The phone must be set"))
        email = self.normalize_email(email)
        user = self.model(phone=phone,  email=email, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, email, fullname, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(phone, email, fullname, password, **extra_fields)


class CustomUser(PermissionsMixin, AbstractBaseUser):
    phone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(_("email address"), blank=True, null=True, unique=True)
    fullname = models.CharField(max_length=150, default='No Name')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email", 'fullname']

    objects = CustomUserManager()

    def __str__(self):
        return self.phone


class UserModel(CustomUser):
    ban = models.BooleanField(default=False)
    profile_image = models.ImageField('user/profiles', blank=True, null=True)
    register_date = jmodels.jDateTimeField(auto_now_add=True)
    post_code = models.CharField(max_length=10, validators=[MinLengthValidator(10)], null=True)
    address = models.TextField()
    designation = models.CharField(max_length=10000, null=True, blank=True)
    is_auther = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.phone} - {self.fullname}'


class UserAddressModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user_address')
    state = models.CharField(max_length=1000)
    city = models.CharField(max_length=1000)
    address = models.TextField()
    plaque = models.IntegerField()
    post_code = models.CharField(max_length=10)
    position_x = models.FloatField()
    position_y = models.FloatField()

    def __str__(self):
        return f'{self.user.phone}  - {self.user.fullname} - {self.address}'
