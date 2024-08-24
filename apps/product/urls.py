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



    path('comment/<product_id>/', ProductCommentView.as_view()),
    path('compare/<category>', CompareView.as_view(), name='compare'),
    path('change/<id>', ProductChangeView.as_view()),
    path('delete/<id>', ProductDeleteView.as_view()),
    path('show/<id>', ShowProductView.as_view()),
    path('chart/<id>', ProductChartView.as_view()),
]
