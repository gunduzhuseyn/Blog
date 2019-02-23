from django.urls import path, re_path
from django.views.generic import TemplateView
from .views import HomeView, PostDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home_url'),
    path('about/', TemplateView.as_view(template_name='myblog/about.html'), name='about_me_url'),
    re_path('^posts/(?P<pk>[^/]+)', PostDetailView.as_view(), name='post_detail_url'),
    re_path('^category/(?P<category_name>[-\w]+)/$', HomeView.as_view(), name='home_with_category_url'),
    path('contact/', TemplateView.as_view(template_name='myblog/contact.html'), name='contact_url'),
]
