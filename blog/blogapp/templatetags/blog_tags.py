# coding = utf-8
from django import template
from ..models import *
from django.db.models.aggregates import Count

register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-create_date')[:num]


@register.simple_tag
def archives():
    return Post.objects.dates('create_date', 'month', order='DESC')


@register.simple_tag
def get_category():
    return Category.objects.all()


@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
# @register.simple_tag
# def get_categories():
#     # 记得在顶部引入 count 函数
#     # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
#     return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tag():
    return Tag.objects.all()
