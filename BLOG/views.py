from django.shortcuts import render,get_object_or_404
from .models import BlogPost,Category,Tag
from django.http import HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from .forms import NewBlogForm,EditBlogForm
from django.contrib.auth.decorators import login_required
import markdown
from django.views.generic import ListView,DetailView
from django.db.models import F
from markdown.extensions.toc import TocExtension#美化自动生成的文章目录点击后的url的显示
from django.utils.text import slugify#这个方法可以很好的处理中文，因为我们的文章目录一般是中文的
# Create your views here.

#用于检测编辑博客的用户是否是这个条博客的所有者
def check_blog_owner(instance,request):
    if instance.owner!=request.user:
        raise Http404

# def index(request):
#     #向所有用户展示博文
#     blogs=BlogPost.objects.order_by('-date_added')
#     # blogs=BlogPost.objects.filter(owner=request.user).order_by('date_added')
#     context={'blogs':blogs}
#     return render(request,'BLOG/index.html',context)

class IndexView(ListView):
    """docstring for IndexView"""
    model=BlogPost
    template_name='BLOG/index.html'
    context_object_name='blogs'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 2

    def get_context_data(self,**kwargs):
        # 首先获得父类生成的传递给模板的字典。
        context=super().get_context_data(**kwargs)
        #调用父类的方法之后context中，父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator,page,is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self,paginator,page,is_paginated):
        #这个函数返回的是一个字典，去和父类的context结合起来传递给模版
        if not is_paginated:
            return {}

        # 当前页左边连续的页码号，初始值为空
        left=[]
        
        # 当前页右边连续的页码号，初始值为空
        right=[]

        #标示第一页页码后是否需要省略号
        left_has_more=False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more=False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first=False
        #同理
        last=False

        # 获得用户当前请求的页码号
        page_number=page.number

        # 获得分页后的总页数
        total_pages=paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range=paginator.page_range#这三个属性都是paginator对象和分页对象的固有属性

        if page_number==1:
            right=page_range[page_number:page_number+2]

            if right[-1] < total_pages-1:
                right_has_more=True
            if right[-1] < total_pages:
                last=True

        elif page_number==total_pages:
            left=page_range[page_number-3 if page_number-3 >0 else 0:page_number-1 ]
            
            if left[0]>2:
                left_has_more=True

            if left[0]>1:
                first=True

        else:#用户请求不是第一页也不是最后一页的情况
            left=page_range[page_number-3 if page_number-3 >0 else 0:page_number-1 ]
            right=page_range[page_number:page_number+2]

            if left[0] > 2:
                left_has_more=True
            if left[0] > 1:
                first = True

            if right[-1] < total_pages-1 :
                right_has_more=True
            if right[-1] < total_pages:
                last= True

        data= {
              'left':left,
              'right':right,
              'left_has_more':left_has_more,
              'right_has_more':right_has_more,
              'first':first,
              'last':last,
        }
        return data#最后返回data这个字典，在用context的方法update更新到context，传递给模版

        


@login_required#只有登录之后才能添加博文
def add_blog(request):
    if request.method!='POST':
        titleform=NewBlogForm()
    else:
        titleform=NewBlogForm(data=request.POST)
        if titleform.is_valid():
            newblog=titleform.save(commit=False)#如果没有这一参数，那么也是直接生成新的模型实例，并且保存到数据库中
            newblog.owner=request.user
            newblog.save()#这个save方法是模型实例的save方法，保存到数据库中
            return HttpResponseRedirect(reverse('BLOG:index'))
    context={'titleform':titleform}
    return render(request,'BLOG/add_blog.html',context)

@login_required
def edit_blog(request,blog_id):
    # blog=BlogPost.objects.get(id=blog_id)
    blog=get_object_or_404(BlogPost,id=blog_id)
    #这个是上面自己定义的一个函数用来检查的，传入第一个参数是实例
    check_blog_owner(blog,request)
    if request.method!='POST':
        titleform=EditBlogForm(instance=blog)
    else:
        titleform=EditBlogForm(instance=blog,data=request.POST)
        if titleform.is_valid():
            titleform.save()
            return HttpResponseRedirect(reverse('BLOG:index'))
    context={'titleform':titleform,'blog':blog}
    return render(request,'BLOG/edit_blog.html',context)

def readmore(request,slug):
    blog=get_object_or_404(BlogPost,slug=slug)
    blog.views_increase()
    # blog.update(views=F('views')+1)
    #markdown渲染博客的内容text
    md= markdown.Markdown(extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     TocExtension(slugify=slugify),
                                  ])
    blog.text=md.convert(blog.text)
    blog.toc=md.toc
    context={'blog':blog}
    return render(request,'BLOG/readmore.html',context)

#用基于类的通用视图listview来重写readmore，测试成功
# class ReadmoreView(DetailView):
#     model = BlogPost
#     template_name = "BLOG/readmore.html"
#     context_object_name='blog'

#     归档
def archives(request,year,month):
    blogs=BlogPost.objects.filter(date_added__year=year,
                                  date_added__month=month
                                  ).order_by('-date_added')
    context={'blogs':blogs}
    return render(request, 'BLOG/index.html', context)

def category(request,pk):
    cate=get_object_or_404(Category,pk=pk)
    blogs=BlogPost.objects.filter(category=cate
                                ).order_by('-date_added')
    context={ 'blogs':blogs }
    return render(request, 'BLOG/index.html',context)

def tag(request,pk):
    # tag=get_object_or_404(Tag,pk=pk)
    blogs=BlogPost.objects.filter(tags__pk=pk
                        ).order_by('-date_added')
    context={'blogs':blogs }
    return render (request, 'BLOG/index.html', context)