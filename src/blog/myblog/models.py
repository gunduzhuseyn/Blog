from django.db import models

import datetime


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.title
