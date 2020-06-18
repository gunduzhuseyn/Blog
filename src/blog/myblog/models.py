# TODO:
# - Make sure media is deleted once the owner model is also deleted

from django.db import models
from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.dispatch import receiver
from django.utils.text import slugify

import datetime
import os


def post_header_image_path(instance, filename):
    return 'posts/{0}/header_image.jpg'.format(instance.slug)


def category_header_image_path(instance, filename):
    return 'categories/{0}/header_image.jpg'.format(instance.slug)


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True, default='')
    slug = models.SlugField(unique=True, blank=True)
    tag_line = models.CharField(max_length=300, null=True, default='')
    header_image = models.ImageField(upload_to=category_header_image_path, null=True, max_length=500)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=150, default='')
    subtitle = models.CharField(max_length=150, default='')
    slug = models.SlugField(unique=True, blank=True, max_length=150)
    body = MarkdownxField()
    date_created = models.DateField(default=datetime.date.today)
    date_published = models.DateField(default=datetime.date.today)
    is_published = models.BooleanField(default=False)
    header_image = models.ImageField(upload_to=post_header_image_path, null=True, max_length=500)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    @property
    def formatted_markdown(self):
        return markdownify(self.body)


def create_unique_slug(instance, class_name, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    if class_name == 'Post':
        qs = Post.objects.filter(slug=slug).order_by('-id')
    else:
        qs = Category.objects.filter(slug=slug).order_by('-id')

    if qs.exists():
        new_slug = '{}-{}'.format(slug, qs.first().id)
        return create_unique_slug(instance, class_name, new_slug=new_slug)
    return slug


@receiver(models.signals.pre_save, sender=Post)
def add_slug_to_post(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = create_unique_slug(instance, 'Post')


@receiver(models.signals.pre_save, sender=Category)
def add_slug_to_category(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = create_unique_slug(instance, 'Category')


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    message = models.TextField(max_length=1000)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name) + "\t" + str(self.email) + "\t" + str(self.time)


# Below code has been taken from the following django snippet:
# https://djangosnippets.org/snippets/10638/
@receiver(models.signals.pre_save, sender=Post)
@receiver(models.signals.pre_save, sender=Category)
def auto_delete_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_image = sender.objects.get(pk=instance.pk).header_image
    except sender.DoesNotExist:
        return False

    new_image = instance.header_image
    if not old_image == new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


@receiver(models.signals.post_delete, sender=Post)
@receiver(models.signals.post_delete, sender=Category)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    if instance.header_image:
        if os.path.isfile(instance.header_image.path):
            os.remove(instance.header_image.path)
