from pyexpat import model
from django.shortcuts import render,redirect
from app01 import models
from django import forms

from app01.utils.form import AdminModelForm,AdminEditModelForm,AdminResetModelForm
from app01.utils.pagination import Pagination 
# Create your views here.
def admin_list(request):
    """管理员列表"""
    #添加搜索功能
    data_dict={}
    search_data=request.GET.get('q','')
    if search_data:
        data_dict['username__contains']=search_data 
    queryset=models.Admin.objects.filter(**data_dict).order_by('-id')  
    #封装分页
    page_object=Pagination(request,queryset)    
    context={
        'queryset':page_object.page_queryset,
        'search_data':search_data,
        'page_string':page_object.html(),
    }
    return render(request,'admin_list.html',context)
def admin_add(request):
    """添加管理员"""
    title='新建管理员'
    if request.method=="GET":
        form=AdminModelForm()
        return render(request,'admin_add.html',{
            'form':form,
            'title':title
        })
    #用户POST提交数据,数据校验    
    form=AdminModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        #{'username':'****','password':'123','confirm_password':'333'}
        form.save()
        #重定向回管理员列表
        return redirect('/admin/list/')
    #校验失败
    return render(request,'admin_add.html',{
        'form':form,
        'title':title
    })
def admin_edit(request,nid):
    """编辑管理员"""
    #根据ID去数据库获取要编辑的那一行数据(对象)
    #对象/None
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        #return redirect('/admin/list/')
        return render(request,'error.html',{'msg':'数据不存在'})
    title='编辑管理员'
    if request.method=="GET":
        form=AdminEditModelForm(instance=row_object)
        return render(request,'admin_edit.html',{
            'form':form,
            'title':title
        })
    #用户POST提交数据,数据校验
    form=AdminEditModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        #重定向回管理员列表
        return redirect('/admin/list/')
    #重定向回
    return render(request,'admin_edit.html',{
        'form':form,
        'title':title
    })
def admin_delete(request,nid):
    """删除管理员"""
    models.Admin.objects.filter(id=nid).delete()
    #重定向回管理员列表
    return redirect('/admin/list/')
def admin_reset(request,nid):
    """重置密码"""
    #根据ID去数据库获取要编辑的那一行数据(对象)
    #对象/None
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')
        #return render(request,'error.html',{'msg':'数据不存在'})
    title='重置密码-{}'.format(row_object.username)
    if request.method=="GET":
        form=AdminResetModelForm()
        return render(request,'change.html',{
            'form':form,
            'title':title
        })
    #用户POST提交数据,数据校验
    form=AdminResetModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        #重定向回管理员列表
        return redirect('/admin/list/')
    #重定向回
    return render(request,'change.html',{
        'form':form,
        'title':title
    })