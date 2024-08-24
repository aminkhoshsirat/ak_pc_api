from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', BlogView.as_view(), name='blog'),
    path('category/<category>', BlogView.as_view(), name='category'),
    path('auther/<url>', AutherView.as_view(), name='auther'),
    path('detail/<slug>', BlogDetailView.as_view(), name='detail_blog'),
    path('comment/<id>', BlogCommentView.as_view()),
    path('tag/<keyword>', BlogView.as_view(), name='keyword'),
]
