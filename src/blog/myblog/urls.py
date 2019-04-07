from django.urls import path, re_path
from django.views.generic import TemplateView
from .views import HomeView, PostDetailView, ContactFormView, ContactSuccessView

urlpatterns = [
    path('', HomeView.as_view(), name='home_url'),
    path('about/', TemplateView.as_view(template_name='myblog/about.html'), name='about_me_url'),
    re_path('^posts/(?P<slug>[-\w]+)$', PostDetailView.as_view(), name='post_detail_url'),
    re_path('^category/(?P<slug>[-\w]+)/$', HomeView.as_view(), name='home_with_category_url'),
    path('contact/', ContactFormView.as_view(), name='contact_url'),
    path('contact/success/', ContactSuccessView.as_view(), name='contact_success_url'),
]
