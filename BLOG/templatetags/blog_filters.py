from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import re 

register = template.Library()

@register.filter#(needs_autoescape=True)#如果没有制定名字name='spacify'，会默认以函数的名字来命名
@stringfilter
def spacify(value,autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x : x
    return mark_safe(re.sub('\s','&'+'nbsp;',esc(value)))
#装饰器后的参数needs_autoescape=True也可以写为
spacify.needs_autoescape = True
