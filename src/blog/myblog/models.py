from django.db import models
from django.urls import reverse
import datetime


class Post(models.Model):
    title = models.CharField(max_length=100, default='')
    subtitle = models.CharField(max_length=100, default='')
    body = models.TextField(default='')
    created_date = models.DateField(default=datetime.date.today)
    published_date = models.DateField(default=datetime.date.today)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'pk': self.id})
