from django.db import models
from django.urls import reverse
from django.conf import settings

import datetime
import os


def post_header_image_dir(instance, filename):
    return '{0}/header_image.jpg'.format(instance.id)


class Post(models.Model):
    title = models.CharField(max_length=100, default='')
    subtitle = models.CharField(max_length=100, default='')
    body = models.TextField(default='')
    date_created = models.DateField(default=datetime.date.today)
    date_published = models.DateField(default=datetime.date.today)
    is_published = models.BooleanField(default=False)
    header_image = models.ImageField(upload_to=post_header_image_dir, null=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if getattr(self, 'header_image_changed', True):
            old_header_image = Post.objects.get(id=self.id).header_image
            if old_header_image:
                path = old_header_image.path
                print(path)
                os.remove(path)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'pk': self.id})
