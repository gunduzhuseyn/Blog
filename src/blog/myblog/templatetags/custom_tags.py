from ..models import Category
from django import template

register = template.Library()


@register.inclusion_tag('myblog/category_list.html')
def show_categories():
    categories = Category.objects.all()
    return {'categories': categories}
