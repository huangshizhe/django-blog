from django.shortcuts import render 
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.decorators import login_required
# Create your views here.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('BLOG:index'))

def register(request):
    '''注册新用户'''
    if request.method!='POST':
        form=UserCreationForm()
    else:
        #处理在模版填写好返回来的表单
        form=UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user=form.save()
            #authenticate返回的是一个用户对象 将他保存在authenticated_user中    
            authenticated_user=authenticate(username=new_user.username,password=request.POST['password1'])
            login(request,authenticated_user)
            return HttpResponseRedirect(reverse('BLOG:index'))
    context={'form':form}
    return render(request,'user/register.html',context)