from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='myblog/index.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='myblog/about.html'), name='about_me'),
    path('post', TemplateView.as_view(template_name='myblog/post.html'), name='post'),
    path('contact/', TemplateView.as_view(template_name='myblog/contact.html'), name='contact'),
]
