from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from django.shortcuts import get_object_or_404

from .models import Post, Category
from .forms import ContactForm


class HomeView(ListView):
    model = Post
    template_name = 'myblog/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        if slug:
            category = get_object_or_404(Category, slug=slug)
            context['category'] = category

        return context

    def get_queryset(self):
        category_name = self.kwargs.get('category_name')
        if category_name:
            category = get_object_or_404(Category, name=category_name)
            return Post.objects.filter(categories=category, is_published=True).order_by('-date_published')

        return Post.objects.filter(is_published=True).order_by('-date_published')


class PostDetailView(DetailView):
    model = Post
    template_name = 'myblog/post_detail.html'
    context_object_name = 'post'


class ContactFormView(FormView):
    template_name = 'myblog/contact.html'
    form_class = ContactForm
    success_url = 'success'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = 'myblog/contact_success.html'
