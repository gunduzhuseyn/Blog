from django.contrib import admin
from .models import Post, Category, Contact
from django.db import models

from martor.widgets import AdminMartorWidget


class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Contact)
