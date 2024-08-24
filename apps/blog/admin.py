from django.contrib import admin
from .models import *


@admin.register(BlogCategoryModel)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(BlogKeyWordModel)
class BlogKeyWordAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(BlogModel)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'published_date', 'read_time', 'conclusion']


@admin.register(BlogLikeModel)
class BlogLikeAdmin(admin.ModelAdmin):
    list_display = ['blog', 'user', 'like', 'dislike']


@admin.register(BlogCommentModel)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = (['user', 'blog', 'text', 'parent'])


@admin.register(BannerBlogModel)
class BannerBlogAdmin(admin.ModelAdmin):
    list_display = ['blog']


@admin.register(AutherModel)
class AutherAdmin(admin.ModelAdmin):
    list_display = []

