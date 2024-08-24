from django.shortcuts import get_object_or_404, HttpResponse, render
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import FormMixin
from django.db.models.aggregates import Count
from utils.services import get_client_ip
from django.utils import timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import Response
from rest_framework.pagination import LimitOffsetPagination
from .serializers import *
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django.db.models import Q


class BlogView(ListView):
    model = BlogModel
    template_name = 'blog/blog.html'
    paginate_by = 15
    context_object_name = 'blogs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = BlogModel.objects.prefetch_related('blog_comments').filter(active=True)

        blog_categories = BlogCategoryModel.objects.filter(active=True)
        context['popular_blogs'] = blogs.order_by('-like')[:15]
        context['most_view_blogs'] = blogs.order_by('-view_count')[:15]
        context['suggested_blogs'] = SuggestedBlogModel.objects.all().order_by('order')[:15]
        context['keywords'] = BlogKeyWordModel.objects.all()[0:15]
        context['blog_categories'] = blog_categories
        return context

    def get_queryset(self):
        category_url = self.kwargs.get('category')
        keyword = self.kwargs.get('keyword')
        search = self.request.GET.get('search')

        blogs = BlogModel.objects.prefetch_related('blog_view', 'blog_likes').filter(active=True)

        if search:
            blogs = blogs.objects.annotate(similar=Greatest(
                TrigramSimilarity('title', search),
                TrigramSimilarity('url', search),
                TrigramSimilarity('category__title', search),
            )).filter(similar__gt=0.1).order_by('-similar')

        if category_url:
            blogs = blogs.filter(category__url=category_url)

        if keyword:
            blogs = blogs.filter(keyword__url=keyword)
        return blogs


class BlogDetailView(DetailView):
    template_name = 'blog/blog_detail.html'
    model = BlogModel
    queryset = BlogModel.objects.prefetch_related('blog_comments').filter(active=True)
    context_object_name = 'blog'
    slug_field = 'url'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        ip = get_client_ip(self.request)
        user = self.request.user

        if user.is_authenticated:
            blog_view, created = BlogViewModel.objects.get_or_create(blog_id=self.get_object().id, user=user, ip=ip)
            blog_view.date_view = timezone.now()
            blog_view.save()
        else:
            blog_view, created = BlogViewModel.objects.get_or_create(blog_id=self.get_object().id, user=None, ip=ip)
            blog_view.date_view = timezone.now()
            blog_view.save()

        context = super().get_context_data(**kwargs)
        comments = context['blog'].blog_comments.prefetch_related('comment_child').filter(active=True, parent=None)
        context['comments'] = comments
        context['comments_count'] = context['blog'].blog_comments.filter(active=True).count
        blogs = BlogModel.objects.filter(active=True)
        context['most_view_blogs'] = blogs.order_by('-view_count')[:5]
        context['new_blogs'] = blogs.order_by('-published_date')[:5]
        context['tags'] = BlogKeyWordModel.objects.all()[:20]
        context['likely_blogs'] = blogs.filter(category=context['blog'].category)
        return context


class BlogCommentView(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            id = int(id)

        except:
            return HttpResponse('unkhown')

        blog = get_object_or_404(BlogModel, id=id)
        comments = blog.blog_comments.prefetch_related('comment_child').filter(active=True, parent=None)
        context = {
            'blog': blog,
            'comments': comments,
            'comments_count': blog.blog_comments.filter(active=True).count,
        }
        return render(request, 'blog/comments.html', context)

    def post(self, request, id):
        try:
            id = int(id)

        except:
            return HttpResponse('unkhown')

        blog = get_object_or_404(BlogModel, id=id)
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user
            text = cd['text']
            parent = None
            replay_to = cd['replay_to']
            if replay_to:
                parent = get_object_or_404(BlogCommentModel, id=replay_to)
            BlogCommentModel.objects.create(user=user, blog=blog, text=text, parent=parent)

            return HttpResponse('success')

        return HttpResponse('failed')


class BlogDetailApiView(RetrieveAPIView):
    serializer_class = BlogSerializers
    queryset = BlogModel.objects.prefetch_related('blog_comments').filter(active=True)
    lookup_field = 'url'
    lookup_url_kwarg = 'slug'

    def get_serializer_context(self):
        # get blog view
        ip = get_client_ip(self.request)
        user = self.request.user
        if user.is_authenticated:
            blog_view, created = BlogViewModel.objects.get_or_create(blog_id=self.get_object().id, user=user, ip=ip)
            blog_view.date_view = timezone.now()
            blog_view.save()
        else:
            blog_view, created = BlogViewModel.objects.get_or_create(blog_id=self.get_object().id, user=None, ip=ip)
            blog_view.date_view = timezone.now()
            blog_view.save()

        context = super().get_serializer_context()
        print(context)
        comments = self.get_object().blog_comments.prefetch_related('comment_child').filter(active=True, parent=None)
        context['comments'] = BlogCommentSerializers(comments, many=True)
        return context

    def post(self, request, slug):
        parent = ''
        replay_to = request.data.get('parent')

        if replay_to:
            parent = replay_to

        data = {
            'blog': self.get_object().id,
            'user': request.user.id,
            'text': request.data['text'],
            'parent': parent,
        }
        comment = BlogCommentSerializers(data=data)
        if comment.is_valid():
            comment.save()
            return Response(comment.data)
        return Response(comment.errors)


class TagApiView(ListAPIView):
    serializer_class = BlogKeyWordSerializers

    def get_queryset(self):
        keyword = self.kwargs.get('keyword')
        tag = get_object_or_404(BlogKeyWordModel, url=keyword)
        blogs = tag.blog_keywords.filter(active=True)
        return blogs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        keyword = self.kwargs.get('keyword')
        tag = get_object_or_404(BlogKeyWordModel, url=keyword)
        context['tag'] = tag
        return context


class AutherView(ListView):
    model = BlogModel
    template_name = 'blog/author.html'
    paginate_by = 15
    context_object_name = 'blogs'

    def get_queryset(self):
        auther_url = self.kwargs.get('url')
        self.extra_context = {'auther': get_object_or_404(AutherModel, url=auther_url, active=True)}
        blogs = BlogModel.objects.annotate(count_view=Count('blog_view')).filter(auther__url=auther_url,
                                                                                 active=True).order_by('-count_view')
        return blogs


class AutherPaginationClass(LimitOffsetPagination):
    page_size = 15


class AutherApiView(ListAPIView):
    serializer_class = BlogSerializers
    pagination_class = AutherPaginationClass


    def get_queryset(self):
        auther_url = self.kwargs.get('url')
        blogs = BlogModel.objects.annotate(count_view=Count('blog_view')).filter(auther__url=auther_url,
                                                                                 active=True).order_by('-count_view')
        return blogs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        auther_url = self.kwargs['url']
        context['auther'] = AutherSerializers(get_object_or_404(AutherModel, url=auther_url, active=True))
        return context


#----------------------------------------Api Views---------------------------------------------

class BlogAPIView(ListAPIView):
    queryset = BlogModel.objects.prefetch_related('blog_view', 'blog_likes', 'blog_comments').filter(active=True)

    def get_queryset(self):
        category_url = self.kwargs.get('category')
        if category_url:
            blogs = BlogModel.objects.prefetch_related('blog_view', 'blog_likes').filter(active=True,
                                                                                         category__url=category_url)
        else:
            blogs = BlogModel.objects.prefetch_related('blog_view', 'blog_likes').filter(active=True)
        return blogs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        blogs = (BlogModel.objects.prefetch_related('blog_view', 'blog_likes').
                 annotate(count_likes=Count('blog_likes'), count_views=Count('blog_view')).filter(active=True))
        blog_categories = BlogCategorySerializers(BlogCategoryModel.objects.filter(active=True), many=True)
        context['popular_blogs'] = BlogSerializers(blogs.order_by('-count_likes')[0: 15], many=True)
        context['most_view_blogs'] = BlogSerializers(blogs.order_by('-count_views')[0:15], many=True)
        context['suggested_blogs'] = SuggestedBlogSerializers(SuggestedBlogModel.objects.all().order_by('order')[0:15],
                                                              many=True)
        context['keywords'] = BlogKeyWordSerializers(BlogKeyWordModel.objects.all()[0:15], many=True)
        context['blog_categories'] = blog_categories
        context['banner_blog1'] = BannerBlogSerializers(get_object_or_404(BannerBlogModel, place='place1'))
        context['banner_blog2'] = BannerBlogSerializers(get_object_or_404(BannerBlogModel, place='place2'))
        context['banner_blog3'] = BannerBlogSerializers(get_object_or_404(BannerBlogModel, place='place3'))
        context['banner_blog4'] = BannerBlogSerializers(get_object_or_404(BannerBlogModel, place='place4'))
        return context
