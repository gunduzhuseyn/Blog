from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Post


class HomeView(ListView):
    model = Post
    template_name = 'myblog/index.html'
    context_object_name = 'posts'
    paginate_by = 20
    ordering = ['published_date']

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class PostDetailView(DetailView):
    model = Post
    template_name = 'myblog/post_detail.html'
    context_object_name = 'post'
