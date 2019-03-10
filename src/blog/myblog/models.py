# TODO:
# - Make sure media is deleted once the owner model is also deleted

from django.db import models
from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

import datetime
import os


def post_header_image_path(instance, filename):
    return 'posts/{0}/header_image.jpg'.format(instance.id)


def category_header_image_path(instance, filename):
    return 'categories/{0}/header_image.jpg'.format(instance.name)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, default='')
    tag_line = models.CharField(max_length=300, null=True, default='')
    header_image = models.ImageField(upload_to=category_header_image_path, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if getattr(self, 'header_image_changed', True):
            category = Category.objects.filter(id=self.id)
            if category and category[0].header_image:
                os.remove(category[0].header_image.path)
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=100, default='')
    subtitle = models.CharField(max_length=100, default='')
    body = MarkdownxField()
    date_created = models.DateField(default=datetime.date.today)
    date_published = models.DateField(default=datetime.date.today)
    is_published = models.BooleanField(default=False)
    header_image = models.ImageField(upload_to=post_header_image_path, null=True)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if getattr(self, 'header_image_changed', True):
            post = Post.objects.filter(id=self.id)
            if post and post[0].header_image:
                os.remove(post[0].header_image.path)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'pk': self.id})

    @property
    def formatted_markdown(self):
        return markdownify(self.body)


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    message = models.TextField(max_length=1000)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name) + "\t" + str(self.email) + "\t" + str(self.time)
