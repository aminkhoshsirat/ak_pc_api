from django.shortcuts import render
from django.views.generic import View, DetailView


class VideoView(View):
    def get(self, request):
        return render(request, 'video/index.html')


class VideoDetailView(DetailView):
    template_name = ''
    slug_url_kwarg = 'url'
