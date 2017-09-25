from django import forms
from .models import BlogPost
class NewBlogForm(forms.ModelForm):
    class Meta:
        model=BlogPost
        #使得表单输入的数据对应到模块Topic中的title和text属性
        fields=['title','text']
        labels={'title':'博客标题','text':'博客内容'}
        #这一句是可以设置表单输入文本框大小的
        #也可以在html中
        #<div class="col-md-4">
    #     <label for="{{ form.name.id_for_label }}">名字：</label>
    #     {{ form.name }}
    #     {{ form.name.errors }}
    #    </div>
        widgets={'title':forms.TextInput(attrs={'size':'50'}),'text':forms.Textarea(attrs={'cols':80})}#attr这个是设置为80列，默认为40列

class EditBlogForm(forms.ModelForm):
    class Meta:
        model=BlogPost
        fields=['title','text']
        labels={'title':'博客标题','text':'博客内容'}
        widgets={'title':forms.TextInput(attrs={'size':'50'}),'text':forms.Textarea(attrs={'cols':80})}