# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
# Create your models here.

# 模型类需要标签，文章正文和三个模型类，正文关联标签和分类，一对多的关系


@python_2_unicode_compatible
class Tag(models.Model):
    # 只需要一个name字段
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


# 装饰器会自动兼容python2
@python_2_unicode_compatible
class Post(models.Model):
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogapp:detail', kwargs={'pk': self.pk})

    title = models.CharField(max_length=70)
    body = models.TextField()
    # 创建时间和修改时间
    create_date = models.DateTimeField()
    update_date = models.DateTimeField()
    # 文章摘要字段，介绍文章前段内容
    excerpt = models.CharField(max_length=200, default=True)
    # 关联标签和分类字段，一篇文章对应多个标签，一个标签对应多个文章，多对多的关系
    # 分类一篇文章属于一个分类一个分类对应多个文章，一对多关系
    tag = models.ManyToManyField('Tag', blank=True)

    category = models.ForeignKey('Category')

    views = models.PositiveIntegerField(default=0)

    # 作者字段，使用django内部应用，处理网站的注册和登陆，内部自动关联的作者，一个文章对应一个作者，一个作者可能多篇文章，多对多的关系

    user = models.ForeignKey(User)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        ordering = ['-create_date']


