# coding = utf-8
from django.db import models
from django.utils.six import python_2_unicode_compatible

# Create your models here.

# 设计模型类，有名字，邮箱，url地址，创建时间，文本，关联文章字段，一篇文章有多个评论，一对多的关系。


@python_2_unicode_compatible
class Comment(models.Model):

    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    post = models.ForeignKey('blogapp.Post')

    def __str__(self):
        return self.text[:20]



