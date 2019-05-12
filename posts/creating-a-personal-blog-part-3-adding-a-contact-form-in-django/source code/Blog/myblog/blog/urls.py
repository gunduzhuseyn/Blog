from django.urls import path
from django.views.generic import TemplateView

from .views import ContactFormView

urlpatterns = [
    path('index/', TemplateView.as_view(template_name='blog/index.html'), name='index_url'),
    path('about/', TemplateView.as_view(template_name='blog/about.html'), name='about_url'),
    path('contact/', ContactFormView.as_view(), name='contact_url'),
    path('contact/success/', TemplateView.as_view(template_name='blog/contact_success.html'), name='about_url'),
    path('post/', TemplateView.as_view(template_name='blog/post.html'), name='post_url'),
]