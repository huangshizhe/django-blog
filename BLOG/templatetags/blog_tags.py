from ..models import BlogPost,Category,Tag
from django import template
from django.db.models.aggregates import Count
#实例化一个template.Library的实例
register=template.Library()

#最新文章
@register.simple_tag
def get_recent_posts(num=5):
    #拿到最新的五篇博客
    return BlogPost.objects.all().order_by('-date_added')[:num]

#归档
@register.simple_tag
def archives():
    #date_added时间排序
    return BlogPost.objects.dates('date_added','month',order='DESC')

@register.simple_tag
def get_category():
    return Category.objects.annotate(num_post=Count('blogpost')).filter(num_post__gt=0)

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_post=Count('blogpost')).filter(num_post__gt=0)