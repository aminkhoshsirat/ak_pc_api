from rest_framework import serializers
from .models import *
from apps.user.serializers import UserSerializers


class BlogCategorySerializers(serializers.ModelSerializer):
    child = serializers.StringRelatedField(many=True)
    class Meta:
        model = BlogCategoryModel
        fields = '__all__'


class BlogKeyWordSerializers(serializers.ModelSerializer):
    class Meta:
        model = BlogKeyWordModel
        fields = '__all__'




class AutherFollowingSerializers(serializers.ModelSerializer):
    # auther_following = AutherSerializers(read_only=True, many=True)
    # user_following = UserSerializers(read_only=True, many=True)

    class Meta:
        model = AutherFollowingModel
        fields = '__all__'


class BlogSerializers(serializers.ModelSerializer):
    # auther_blogs = AutherSerializers(read_only=True, many=True)
    # category_blogs = BlogCategorySerializers(read_only=True, many=True)
    # blog_keywords = BlogKeyWordSerializers(read_only=True, many=True)

    class Meta:
        model = BlogModel
        fields = '__all__'


class AutherSerializers(serializers.ModelSerializer):
    auther_blogs = BlogSerializers(read_only=True, many=True)

    class Meta:
        model = BlogCategoryModel
        fields = '__all__'


class BlogLikeSerializers(serializers.ModelSerializer):
    blog_likes = BlogSerializers(read_only=True, many=True)
    user_blog_likes = UserSerializers(read_only=True, many=True)

    class Meta:
        model = BlogLikeModel
        fields = '__all__'


class BlogCommentSerializers(serializers.ModelSerializer):
    user_blog_comments = UserSerializers(read_only=True, many=True)

    class Meta:
        model = BlogCommentModel
        exclude = ['active']


class BlogViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = BlogViewModel
        fields = '__all__'


class SuggestedBlogSerializers(serializers.ModelSerializer):
    class Meta:
        model = SuggestedBlogModel
        fields = '__all__'


class BannerBlogSerializers(serializers.ModelSerializer):
    class Meta:
        models = BannerBlogModel
        fields = '__all__'
