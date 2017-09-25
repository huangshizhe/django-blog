''' 这是应用程序user中的urls'''

from django.conf.urls import url
from django.contrib.auth.views import login#从这里导入login和logout
from . import views

urlpatterns=[
    #登录界面
    url(r'^login/$',login,{'template_name':'user/login.html'},name='login'),
    # 因为我们这里没有自定义视图函数，
    # 所以在视图函数中没有导向我们的html的语句，在这里传入这个字典，
    # 让django知道去哪里找到我们的html文件
    #注销界面
    #这里的视图函数命名这样子是为了和待会导入的logout区别开来
    url(r'^logout/$',views.logout_view,name='logout'),
    url(r'^register/$',views.register,name='register'),
]