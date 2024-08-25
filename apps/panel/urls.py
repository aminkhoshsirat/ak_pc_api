from django.urls import path
from .views import *
from apps.chat.views import AdminChatRoomApiView, AdminChatApiView

app_name = 'panel'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('site-detail', SiteDetailView.as_view(), name='site_detail'),
    path('chat-box', AdminChatRoomApiView.as_view(), name='chat_box'),
    path('chat/<id>', AdminChatApiView.as_view()),
    path('products/', ProductListView.as_view(), name='products'),
    path('products-grid/', ProductGridListView.as_view(), name='products_grid'),
    path('products-grid-body/', ProductGridBodyView.as_view()),
    path('product/add', AddProductView.as_view(), name='products_add'),
    path('product/add-new', AddNewProductView.as_view()),
    path('product/delete/<id>', ProductDeleteView.as_view(), name='products_delete'),
    path('product-categories/', ProductCategoryView.as_view(), name='products_category'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('order/<pk>', OrderDetailView.as_view(), name='order'),
    path('daily-works/', DailyWorksViews.as_view(), name='daily_works'),
    path('calendar/', CalendarView.as_view(), name='calender'),
    path('daily-works/old/', OldDailyWorksViews.as_view(), name='old_works'),
    path('financial-statement', FinancialStatementsView.as_view(), name='financial_statement'),
    path('financial-statement/detail/<pk>', FinancialStatementSingleView.as_view(), name='financial_statement'),
    path('factor-pdf/<id>', FactorPdfView.as_view(), name='factor_pdf'),
    path('faq', FaqView.as_view(), name='faq'),
    path('users', UserListView.as_view(), name='users'),
    path('auther', AutherListView.as_view(), name='auther'),
    path('add-admin', AddAdminView.as_view(), name='add_admin'),
    path('add-user', AddUserView.as_view(), name='add_user'),
    path('add-auther', AddAutherView.as_view(), name='add_auther'),
    path('admin', AdminView.as_view(), name='admin'),
    path('header/', IndexApiView.as_view()),
]
