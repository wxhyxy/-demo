from django.shortcuts import render, HttpResponse, get_object_or_404
import markdown
from .models import *
from comments.forms import *
from django.views.generic import ListView, DetailView
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.db.models import Q
# Create your views here.


# def index(request):
#     post_list = Post.objects.all()
#     return render(request, 'blog/index.html', {'post': post_list})


class IndexViews(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post'

    paginate_by = 1

    ''' 第 1 页页码，这一页需要始终显示。
        第 1 页页码后面的省略号部分。但要注意如果第 1 页的页码号后面紧跟着页码号 2，那么省略号就不应该显示。
        当前页码的左边部分，比如这里的 3-6。
        当前页码，比如这里的 7。
        当前页码的右边部分，比如这里的 8-11。
        最后一页页码前面的省略号部分。但要注意如果最后一页的页码号前面跟着的页码号是连续的，那么省略号就不应该显示。
        最后一页的页码号。'''

    def get_context_data(self, **kwargs):
        # 在类试图函数内使用get_context_date内可以自定义一些自定义的模板变量进去。

        # 首先获得父类生成的传递给模板的字典
        content = super(IndexViews, self).get_context_data(**kwargs)

        # 父类字典中已经生成paginator,page_obj,is_paginated 这三个模板变量
        # content是一个字典对象，可以使用get从中取出某个键对应的值

        # Paginator的实例
        paginator = content.get('paginator')

        # 当前页面分页对象
        page = content.get('page_obj')

        # 是否已经分页
        is_paginated = content.get('is_paginated')

        # 调用自己写的 pageination_data 方法获得显示分页导航条需要的数据
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 content 中，注意paginator_data也是一个字典
        content.update(pagination_data)

        # 更新后返回 content，使用这个字典中的模板变量去渲染模板
        return content

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，返回空字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右面连续的页码号，初始值为空
        right = []

        # 如果标示第1页页码是否需要显示省略号
        left_has_more = False

        # 如果标示最后一页页码是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第1页的页码号。
        # 如有当前页面左边的连续页码中已经含有第一页，此时无需显示第一页页码
        # 其他情况下第一页页码始终需要显示的，初始值为false
        first = False

        # 标示是否需要显示最后一页页码号.
        last = False

        # 获取用户当前请求的页码号
        page_number = page.number

        # 获取分页的总页数
        total_page = paginator.num_pages

        # 获取分页页码列表，比如分了四页，那么就是[1,2,3,4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边不需要数据，因此 left=[],此时获取当前页右边连续页码号，不如分了四页，那么获取的为 right_list = [2,3],可以更改数字获取更多数据
            right = page_range[page_number:page_number+2]

            # 如果最右面的页码比最后一页的页码号减一还小，需要显示省略号，通过right_has_more 显示

            if right[-1] < total_page-1:
                right_has_more = True

            # 如果最右面的页码比最后一页的页码还小，说明右面连续的页码不包含最后一页，显示最后一页页码
            if right[-1] < total_page:
                last = True

        elif page_number == total_page:
            # 如果用户请求最后一页的数据，那么右面不需要数据（默认没有）,此时要获取当前页左连续页码号，比如分四爷那么获取的为left_list = [2,3]
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0: page_number-1]

            # 如果最右面的页码数大于2，需要省略号
            if left[0] > 2:
                left_has_more = True

            # 如果最右面的页码数大于1，则说明左面连续的页码不包含第一页，需要显示第一页

            if left[0] > 1:
                first = True

        else:
            # 用户请求不是第一页也不是最后一页，获取两端连续的页码
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number-1]
            right = page_range[page_number: page_number+2]

            # 是否需要显示最后一页和最后一页省略号
            if right[-1] < total_page-1:
                right_has_more = True
            if right[-1] < total_page:
                last = True

            # 是否显示第一页和省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last
        }

        return data


# class CategoryViews(ListView):
#     module = Post
#     template_name = 'blog/index.html'
#     context_object_name = 'post'
#
#     def get_queryset(self):
#         cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
#         return super(CategoryViews, self).get_queryset().filter(category=cate)


# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post = Post.objects.all().filter(category=cate)
#     return render(request, 'blog/index.html', {'post': post})


class PostDetailView(DetailView):

    model = Post
    context_object_name = 'post'
    template_name = 'blog/detail.html'

    # 调用内部get方法，必须返回一个httpresponse对象
    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 文章引用计数+1
        self.object.increase_views()

        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)

        md = markdown.Markdown( extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          TocExtension(slugify=slugify)
                                      ])
        post.body = md.convert(post.body)
        post.toc = md.toc

        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()

        context.update({'form': form,
                        'comment': comment_list})

        return context


class CategoryViews(IndexViews):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryViews, self).get_queryset().filter(category=cate)


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     post.increase_views()
#
#     post.body = markdown.markdown(post.body,
#             extensions=[
#                 'markdown.extensions.extra',
#                 'markdown.extensions.codehilite',
#                 'markdown.extensions.toc'
#             ]
#     )
#
#     # 评论区做完更新下详情页，传递三个参数，post，comment，form
#     comment_list = post.comment_set.all()
#     form = CommentForm()
#
#     return render(request, 'blog/detail.html', {'post': post, 'form': form, 'comment': comment_list})


# def archives(request, year, month):
#     post_list = Post.objects.all().filter(
#         create_date__year=year,
#         create_date__month=month
#     )
#
#     return render(request, 'blog/index.html', {'post': post_list})


class ArchivesViews(IndexViews):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesViews, self).get_queryset().filter(create_date__year=year,
                                                                create_date__month=month)


class TagViews(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagViews, self).get_queryset().filter(tag=tag)


def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键字'
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg, 'post': post_list})
