# coding=utf-8

from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm
from .models import Comment
from blogapp.models import Post

# Create your views here.


def post_comment(request, post_pk):
    # 获取到评论的详情页，评论和页面关联起来
    post = get_object_or_404(Post, pk=post_pk)

    # 判断请求方式是否为post，如果是post请求则处理表单
    if request.method == 'POST':

        # 用户提交的数据存储在request.POST内，是一个类字典对象，利用这些数据构造CommentForm实例，生成Django表单
        form = CommentForm(request.POST)

        # form.is_vaild()方法，Django会自动判断格式是否符合规则
        if form.is_valid():
            # 符合规则调用表单save方法保存到数据库，comment=false生成模型实例但不保存到数据库
            comment = form.save(commit=False)

            # 将评论和文章关联起来
            comment.post = post

            # 将数据保存到数据库
            comment.save()
            # 重定向到post详情页，rediect函数接收一个模型实例的时候，会调用实例的get_absolute_url，重定向方法返回的url页面中
            return redirect(post)

        # 如果格式不符合规则的话，重新渲染详情页，会传三个模板变量给detial，一个post，一个评论，一个表单
        else:
            comment_list = Post.comment_set.all()
            return render(request, 'blog/detail.html', {'post': post, 'form': form, 'comment': comment_list})
    # 不是post请求，没有数据，重定向到详情页面
    return redirect(post)
