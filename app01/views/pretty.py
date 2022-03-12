from gc import get_objects
from genericpath import exists
from pyexpat import model
from attr import field
from django.shortcuts import render,redirect
from app01 import models
from django import forms
from app01.utils.form import PrettyModelForm
from app01.utils.pagination import Pagination 
############靓号管理############
def pretty_list(request):
    """靓号列表"""
    #添加搜索功能
    data_dict={}
    search_data=request.GET.get('q','')
    if search_data:
        data_dict['mobile__contains']=search_data  
    #封装分页    
    queryset=models.PrettyNum.objects.filter(**data_dict).order_by('-level')
    page_object=Pagination(request,queryset)    
    context={
        'queryset':page_object.page_queryset,
        'search_data':search_data,
        'page_string':page_object.html(),
    }
    return render(request,'pretty_list.html',context)
def pretty_add(request):
    """靓号添加"""
    if request.method=="GET":
        form=PrettyModelForm()
        return render(request,'pretty_add.html',{'form':form})
    #用户POST提交数据,数据校验
    print(request.POST)
    form=PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        #重定向回部门列表
        return redirect('/pretty/list/')
    #校验失败
    return render(request,'pretty_add.html',{'form':form})
def pretty_edit(request,nid):
    """靓号修改"""
    #根据ID去数据库获取要编辑的那一行数据(对象)
    row_object=models.PrettyNum.objects.filter(id=nid).first()
    if request.method=="GET":
        form=PrettyModelForm(instance=row_object)
        return render(request,'pretty_edit.html',{'form':form})
    #用户POST提交数据,数据校验
    form=PrettyModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        #重定向回部门列表
        return redirect('/pretty/list/')
    #重定向回
    return render(request,'pretty_edit.html',{'form':form})
def pretty_delete(request,nid):
    """靓号删除"""
    models.PrettyNum.objects.filter(id=nid).delete()
    #重定向回部门列表
    return redirect('/pretty/list/')
############搜索手机号############
#知识点
#models.PrettyNum.objects.filter(id=12)         #id等于12
#models.PrettyNum.objects.filter(id__gt=12)     #id大于12
#models.PrettyNum.objects.filter(id__gte=12)    #id大于等于12
#models.PrettyNum.objects.filter(id__It=12)     #id小于12
#models.PrettyNum.objects.filter(id__Ite=12)    #id小于等于12

#models.PrettyNum.objects.filter(mobile='999')             #等于
#models.PrettyNum.objects.filter(mobile__startswith='999')  #筛选出以999开头
#models.PrettyNum.objects.filter(mobile__endswith='999')    #筛选出以999结尾
#models.PrettyNum.objects.filter(mobile__contains='999')    #筛选出包含999