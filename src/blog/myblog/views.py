from django.views.generic.list import ListView

from .models import Post


class HomeView(ListView):
    model = Post
    template_name = 'myblog/index.html'
    context_object_name = 'posts'
