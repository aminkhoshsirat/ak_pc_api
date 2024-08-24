import json
from django.shortcuts import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, ListView, DetailView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from apps.blog.models import BlogCommentModel
from apps.bucket.models import BuketModel
from apps.product.models import UserFavoriteProductModel, ProductCommentModel
from .forms import *
from .serializers import *
from django.utils.safestring import mark_safe
from akurtekPC.config import NESHAN_API_KEY
from apps.panel.models import SiteDetailModel
import redis
import random
from apps.notification.models import UserNotificationModel
from django.utils import timezone
from utils.services import send_otp

r = redis.Redis(host='localhost', port=6379, db=0)


class UserLoginView(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phone_or_email = cd['phone_or_email']
            user = UserModel.objects.filter(Q(phone=phone_or_email) | Q(email=phone_or_email)).first()
            if user:
                check_password = user.check_password(cd['password'])
                if check_password:
                    login(request, user)
                    return redirect('index')
                else:
                    messages.add_message(request, messages.ERROR, 'رمز عبور اشتباه است')
                    return redirect(request.META['HTTP_REFERER'])
            else:
                messages.add_message(request, messages.ERROR, 'کاربر یافت نشد')
                return redirect('user:login')
        else:
            return render(request, 'user/login.html')


class UserLoginHeaderView(View):
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phone_or_email = cd['phone_or_email']
            user = UserModel.objects.filter(Q(phone=phone_or_email) | Q(email=phone_or_email)).first()
            if user:
                check_password = user.check_password(cd['password'])
                if check_password:
                    login(request, user)
                    return redirect(request.META['HTTP_REFERER'])
                else:
                    messages.add_message(request, messages.ERROR, 'رمز عبور اشتباه است')
                    return redirect(request.META['HTTP_REFERER'])
            else:
                messages.add_message(request, messages.ERROR, 'کاربر یافت نشد')
                return redirect(request.META['HTTP_REFERER'])
        else:
            return redirect(request.META['HTTP_REFERER'])


class UserRegisterView(View):
    def get(self, request):
        return render(request, 'user/register.html')

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phone = cd['phone']
            user = UserModel.objects.filter(phone=phone).first()
            if user:
                if user.ban:
                    return HttpResponse('کاربر ازسایت محروم شده است')
                return HttpResponse('کاربر وجود دارد')

            else:
                time = r.ttl(f'{phone}:activation_code')
                if time < 420:
                    code = random.randint(100000, 999999)
                    r.set(f'{phone}:activation_code', code, ex=600)
                    send_otp(phone, str(code))
                    return render(request, 'user/send-code.html')
                else:
                    return render(request, 'user/send-code.html')
        else:
            return HttpResponse(form.errors)


class UserRegisterActivationView(View):
    def post(self, request):
        form = UserRegisterActivationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            code = cd['code']
            phone = cd['phone']
            try:
                sending_code = str(int(r.get(f'{phone}:activation_code')))
            except:
                sending_code = ''
            print(sending_code)
            if sending_code:
                if sending_code == code:
                    user = UserModel.objects.create_user(fullname=cd['fullname'], email=cd['email'], phone=phone, password=cd['password'])
                    r.delete(f'{phone}:activation_code')
                    login(request, user)
                    return HttpResponse('ok')
                else:
                    return HttpResponse('code is incorrect')
            return HttpResponse('failed')

        else:
            return render(request, 'user/register.html')


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('index')


class SendOtpCodeView(View):
    def post(self, request):
        form = SendOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phone = cd['phone']
            user = UserModel.objects.filter(phone=phone).first()
            if user:
                if user.ban:
                    messages.add_message(request, messages.ERROR, 'کاربر ازسایت محروم شده است')
                else:
                    time = r.ttl(f'{phone}:activation_code')
                    if time < 420:
                        code = random.randint(100000, 999999)
                        r.set(f'{phone}:activation_code', code, ex=600)
                        send_otp(phone, code)

            else:
                return HttpResponse('کاربر وجود ندارد')

        else:
            return HttpResponse(form.errors)


class PasswordForgetView(View):
    def get(self, request):
        return render(request, 'user/forget.html')

    def post(self, request):
        pass


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user/change-password.html')

    def post(self, request):
        form = UserChangePasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = self.request.user
            password = cd['password']
            user.set_password(password)
            return redirect('user:dashboard')
        return render(request, 'user/change-password.html')


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile.html'

    def post(self, request):
        user = request.user
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()


class UserDashboardView(LoginRequiredMixin, ListView):
    template_name = 'user/dashboard.html'
    model = UserFavoriteProductModel
    paginate_by = 10
    context_object_name = 'products'

    def get_queryset(self):
        products = UserFavoriteProductModel.objects.filter(user=self.request.user)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications = UserNotificationModel.objects.filter(Q(user=self.request.user) | Q(user=None),
                                                             expire_date__gt=timezone.now()).order_by('-published_date')
        context['notifications'] = notifications
        context['orders'] = BuketModel.objects.filter(is_paid=True)
        return context


class UserCommentsView(LoginRequiredMixin, View):
    def get(self, request):
        product_comments = ProductCommentModel.objects.filter(user=request.user)
        blog_comments = BlogCommentModel.objects.filter(user=request.user)
        context = {
            'product_comments': product_comments,
            'blog_comments': blog_comments,
        }
        return render(request, 'user/comments.html', context)


class UserEditProfileView(View):
    def get(self, request):
        return render(request, 'user/edit-profile.html')


class FavoriteView(ListView):
    template_name = 'user/favorite.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        products = UserFavoriteProductModel.objects.filter(user=self.request.user)
        return products


class OrderView(ListView):
    template_name = 'user/order.html'
    context_object_name = 'orders'
    paginate_by = 20

    def get_queryset(self):
        orders = BuketModel.objects.filter(is_paid=True, user=self.request.user)
        return orders


class OrderDetailView(DetailView):
    model = BuketModel
    template_name = 'user/order-detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        orders = BuketModel.objects.prefetch_related('bucket_products').filter(is_paid=True, user=self.request.user)
        return orders


class UserAddressView(ListView):
    template_name = 'user/address.html'
    model = UserAddressModel
    paginate_by = 20
    context_object_name = 'address'

    def get_queryset(self):
        user = self.request.user
        address = UserAddressModel.objects.filter(user=user)
        return address


# class UserAddressView(View):
#     def get(self, request):
#         context = {
#             'api_key': mark_safe(NESHAN_API_KEY),
#             'map_x': request.session.get('map_x'),
#             'map_y': request.session.get('map_y'),
#         }
#         return render(request, 'user/neshan.html', context)
#
#     def post(self, request):
#         form = NeshanSearchForm(request.POST)
#         if form.is_valid():
#             search = form.cleaned_data['search']
#             map = requests.get(f'https://api.neshan.org/v4/geocoding?address={search}', headers={"Api-Key": 'service.a77ead3f22874b168c2b86ed615fd771'})
#             map = map.json()['location']
#             request.session['map_x'] = map['x']
#             request.session['map_y'] = map['y']
#             context = {
#                 'api_key': mark_safe(NESHAN_API_KEY),
#                 'map_x': request.session['map_x'],
#                 'map_y': request.session['map_y'],
#                 'search': search,
#             }
#
#             return render(request, 'user/neshan.html', context)
#
#
class UserAddAddressView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'api_key': mark_safe(NESHAN_API_KEY),
            'map_x': request.session.get('map_x'),
            'map_y': request.session.get('map_y'),
        }
        return render(request, 'user/neshan.html', context)

    def post(self, request):
        count = UserAddressModel.objects.all().count()
        try:
            limit = SiteDetailModel.objects.first().limit_of_address_can_add
        except:
            limit = 5
        if count > limit:
            return HttpResponse(f'امکان اضافه کردن بیش از {limit}وجود ندارد')
        else:
            form = AddressForm(request.POST)

            if form.is_valid():
                cd = form.cleaned_data
                UserAddressModel.objects.create(user=request.user, state=cd['state'], city=cd['city'],
                                                address=cd['address'], plaque=cd['plaque'],
                                                post_code=cd['post_code'], position_x=float(cd['position_x']),
                                                position_y=float(cd['position_y'])).save()
                return HttpResponse('success')
            errors = json.dumps(form.errors)
            return errors


class NotificationView(ListView):
    template_name = 'user/notification.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        notifications = UserNotificationModel.objects.filter(Q(user=self.request.user) | Q(user=None), expire_date__gt=timezone.now()).order_by('-published_date')
        return notifications

# ---------------------------- DRF --------------------------


class LoginView(APIView):
    def post(self, request):
        data = request.data
        user_serializer = LoginSerializers(data=data)

        if user_serializer.is_valid():
            user = UserModel.objects.filter(Q(phone=data['phone_or_email']) | Q(email=data['phone_or_email']))
            if user:
                check_pass = user.check_password(data['password'])

                if check_pass:
                    login(request, user)
                    token = Token(user=user).key
                    return Response({'token': token, 'detail': 'login success'}, status=status.HTTP_202_ACCEPTED)

                else:
                    return Response({'detail': 'password incorrect'}, status=status.HTTP_404_NOT_FOUND)

            else:
                return Response({'detail': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(user_serializer.errors)
