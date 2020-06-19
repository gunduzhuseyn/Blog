from django.urls import path, re_path
from django.views.generic import TemplateView
from .views import HomeView, PostDetailView, ContactFormView

urlpatterns = [
    path('', HomeView.as_view(), name='home_url'),
    path('about/', TemplateView.as_view(template_name='myblog/about.html'), name='about_me_url'),
    re_path('^posts/(?P<slug>[-\w]+)$', PostDetailView.as_view(), name='post_detail_url'),
    re_path('^category/(?P<slug>[-\w]+)/$', HomeView.as_view(), name='home_with_category_url'),
    path('contact/', ContactFormView.as_view(), name='contact_url'),
    path('contact/success/', TemplateView.as_view(template_name='myblog/contact_success.html'),
         name='contact_success_url'),
    path('400.html/', TemplateView.as_view(template_name='400.html'), name='400_error_page'),
    path('403.html/', TemplateView.as_view(template_name='403.html'), name='403_error_page'),
    path('404.html/', TemplateView.as_view(template_name='404.html'), name='404_error_page'),
    path('500.html/', TemplateView.as_view(template_name='500.html'), name='500_error_page'),
]
