from django.urls import path
from .views import *
from  rest_framework_simplejwt.views import TokenBlacklistView

app_name = 'user'

urlpatterns = [
    path('login', LoginApiView.as_view(), name='login'),
    path('logout', TokenBlacklistView.as_view(), name='logout'),
    path('register', UserRegisterApiView.as_view(), name='register'),
    path('register/activate', UserRegisterActivationApiView.as_view()),
    path('send-code', SendOtpCodeApiView.as_view(), name='send_otp_code'),


    path('forget-password', PasswordForgetView.as_view(), name='forget'),
    path('change-password', ChangePasswordView.as_view(), name='change_password'),
    path('dashboard', UserDashboardView.as_view(), name='dashboard'),
    path('edit-profile', UserEditProfileView.as_view(), name='edit_profile'),
    path('favorite', FavoriteView.as_view(), name='favorite'),
    path('notification', NotificationView.as_view(), name='notification'),
    path('profile', UserProfileView.as_view(), name='profile'),
    path('address', UserAddressView.as_view(), name='address'),
    path('add-address', UserAddAddressView.as_view(), name='add_address'),
    path('order', OrderView.as_view(), name='order'),
    path('order/<pk>', OrderDetailView.as_view(), name='order_detail'),

    path('comments', UserCommentsView.as_view(), name='comments'),
]
