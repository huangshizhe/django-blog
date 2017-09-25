from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
# Create your models here.
class BlogPost(models.Model):#注意我这个模型的名称，是Post
    #注意我这个模型的名称，是Post，大写B大写P
    #标题
    title=models.CharField(max_length=200)
    #内容
    text=models.TextField()
    #摘要
    excerpt = models.CharField(max_length=200, blank=True)
    #发表时间
    date_added=models.DateTimeField(auto_now_add=True)
    #文章浏览量,只能是0和正整数,默认初始为0
    views=models.PositiveIntegerField(default=0)
    #多对一 to 目录
    category = models.ForeignKey('Category')#默认定义为id=1的类别
    #多对一 to 作者
    owner=models.ForeignKey(User)
    #多对多 to 标签
    tags = models.ManyToManyField('Tag', blank=True)
    #url
    slug = models.SlugField(
    verbose_name=('固定链接'),
    help_text=('本文章的短网址(Uri identifier).'),
    max_length=255,
    unique=True
    )

    def __str__(self):
        return self.title+self.text
    class Meta:#默认排序
        ordering=['-date_added']
    #blogpost的实例就可以自己生成自己的 URL。
    def get_absolute_url(self):
        return reverse('BLOG:readmore',kwargs={ 'slug':self.slug } )
    #浏览量增加的方法
    def views_increase(self):
        self.views +=1
        self.save( update_fields=['views'] )
    #复写模型的save方法，自动生成摘要
    def save(self,*args,**kwargs):
        if not self.excerpt:
            #实例化一个markdown实例等下来渲染
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            md=markdown.Markdown(extensions=[
                                'markdown.extensions.extra',
                                'markdown.extensions.codehilite',
                                'markdown.extensions.toc'
                                ])
            self.excerpt=strip_tags(md.convert(self.text))[:50]
        #调用父类的save 方法将数据保存到数据库中
        super(BlogPost, self).save(*args, **kwargs)
        

class Category(models.Model):
    name=models.CharField(
        verbose_name=('类别名称'),
        help_text=('文章的类别名'),
        max_length=100,
        )
    # slug=models.SlugField(
    #     verbose_name=('类别链接'),
    #     help_text=('类别的url'),
    #     max_length=50,
    #     default=
    #     )
    def __str__(self):
        return self.name   

class Tag(models.Model):
    name=models.CharField(
        verbose_name=('标签名称'),
        help_text=('文章所属的标签'),
        max_length=50,
        )
    def __str__(self):
        return self.name  
