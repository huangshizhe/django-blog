'''这是在应用程序BLOG中的url文件'''
# 这是处理url函数的
from django.conf.urls import url,include
from . import views
from django.views.static import serve

app_name='BLOG'

urlpatterns = [
    # url(r'^$',views.index,name='index'),
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^add_blog/$',views.add_blog,name='add_blog'),
    url(r'^edit_blog/(?P<blog_id>\d+)/$',views.edit_blog,name='edit_blog'),
    #应用静态图片，当输入locahost:8000/static/images/dGPRgA.jpg时，会自动到document
    #去寻找对应路径F:/BLOG/static/images/dGPRgA.jpg,也就是前面的正则表达式提取并保存在path中
    # url(r'^static/(?P<path>.*)',serve,{'document_root':'F:/BLOG/'} ),
    # url(r'^readmore/(?P<slug>[-\w]+)', views.ReadmoreView.as_view(), name='readmore'),#测试成功
    url(r'^readmore/(?P<slug>[-\w]+)', views.readmore, name='readmore'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.archives,name='archives'),
    url(r'^category/(?P<pk>[\w]+)/$',views.category,name='category'),
    url(r'^tag/(?P<pk>[\w]+)/$',views.tag,name='tag'),
    
]
