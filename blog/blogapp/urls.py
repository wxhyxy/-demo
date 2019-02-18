# coding = utf-8

from django.conf.urls import url
from .views import *

app_name = 'blogapp'
# 试图函数命名空间

urlpatterns = [
    url(r'^$', IndexViews.as_view(), name='index'),
    url(r'^category/(?P<pk>[0-9]+)/$', CategoryViews.as_view(), name='category'),
    url(r'^post/(?P<pk>[0-9]+)/$', PostDetailView.as_view(), name='detail'),
    url(r'^post/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', ArchivesViews.as_view(), name='archives'),
    url(r'^tag/(?P<pk>[0-9]+)', TagViews.as_view(), name='tags'),
    # url(r'^search/$', search, name='search')
]
