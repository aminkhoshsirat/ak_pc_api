from django.urls import path
from .views import *

app_name = 'product'

urlpatterns = [
    path('', ProductListApiView.as_view(), name='product_list_view'),
    path('main-category/<main_category>/', ProductListApiView.as_view(), name='products_main_category'),
    path('child-category/<child_category>/', ProductListApiView.as_view(), name='products_child_category'),
    path('detail/<slug>/', ProductDetailApiView.as_view(), name='product_detail_view'),
    path('like/<id>/', ProductLikeApiView.as_view()),
    path('add/<id>', ProductAddApiView.as_view()),
    path('chart/<id>', ProductChartApiView.as_view()),
    path('show/<id>', ShowProductApiView.as_view()),
    path('change/<id>', ProductChangeApiView.as_view()),
    path('delete/<id>', ProductDeleteApiView.as_view()),
    path('compare/<category>', CompareProductApiView.as_view(), name='compare'),

    path('comment/<product_id>/', ProductCommentView.as_view()),
]
