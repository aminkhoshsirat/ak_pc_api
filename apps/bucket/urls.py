from django.urls import path
from .views import *

app_name = 'bucket'

urlpatterns = [
    path('cart', BucketApiView.as_view(), name='cart'),
    path('pay/', OrderPayView.as_view()),
    path('small-bucket/', SmallBucketView.as_view()),
    path('small-bucket/delete/<id>', DeleteProductBucketView.as_view()),
]