from django.urls import path
from django.views.generic import TemplateView

from .views import HomeView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home_url'),
    path('index/', TemplateView.as_view(template_name='blog/index.html'), name='index_url'),
    path('about/', TemplateView.as_view(template_name='blog/about.html'), name='about_url'),
    path('contact/', TemplateView.as_view(template_name='blog/contact.html'), name='contact_url'),
    path('post/', TemplateView.as_view(template_name='blog/post.html'), name='post_url'),
]