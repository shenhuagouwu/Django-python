from gc import get_objects
from genericpath import exists
from pyexpat import model
from attr import field
from django.shortcuts import render,redirect
from app01 import models
from django import forms
from app01.utils.form import UserModelForm
def user_list(request):
    """用户列表"""
    #从数据库中获取所有用户列表
    queryset=models.UserInfo.objects.all()
    #for item in queryset:
    #    print (item.id,item.name,item.password,item.age,item.account,item.create_time.strftime("%Y-%m-%d"),item.get_gender_display(),item.depart.title)
    return render(request,'user_list.html',{
        'queryset':queryset,
    })
def user_add(request):
    """添加用户"""
    if request.method=="GET":
        context={
            'gender_choices':models.UserInfo.gender_choices,
            'depart_list':models.Department.objects.all()
        }
        return render(request,'user_add.html',context)
    #获取用户POST提交过来的数据
    user=request.POST.get('user')
    pwd=request.POST.get('pwd')
    age=request.POST.get('age')
    account=request.POST.get('ac')
    ctime=request.POST.get('ctime')
    gender_id=request.POST.get('gd')
    depart_id=request.POST.get('dp')
    #保存到数据库
    models.UserInfo.objects.create(name=user,password=pwd,age=age,account=account,create_time=ctime,gender=gender_id,depart_id=depart_id)
    #重定向回部门列表
    return redirect('/user/list/')
############ Form 示例,不针对数据库 ############
############ ModelForm 示例,针对数据库中的某个表 ############
def user_modelformadd(request):
    """添加用户(ModelForm版本)"""
    if request.method=="GET":
        form=UserModelForm()
        return render(request,'user_modelformadd.html',{'form':form})
    #用户POST提交数据,数据校验
    form=UserModelForm(data=request.POST)
    if form.is_valid():
        #如果数据合法，保存到数据库
        #print(form.cleaned_data)
        #models.UserInfo.objects.create()
        form.save()
        #重定向回部门列表
        return redirect('/user/list/')
    #校验失败
    return render(request,'user_modelformadd.html',{'form':form})
def user_edit(request,nid):
    """编辑用户"""
    #根据ID去数据库获取要编辑的那一行数据(对象)
    row_object=models.UserInfo.objects.filter(id=nid).first()
    if request.method=="GET":
        form=UserModelForm(instance=row_object)
        return render(request,'user_edit.html',{'form':form})
    #用户POST提交数据,数据校验
    form=UserModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        #如果数据合法，保存到数据库(默认保存的是用户输入的所有数据)
        #如果要保存的不是用户输入的可以用（form.instance.字段名=值）
        form.save()
        #重定向回部门列表
        return redirect('/user/list/')
    #重定向回部门列表
    return render(request,'user_edit.html',{'form':form})
def user_delete(request,nid):
    """删除部门"""
    models.UserInfo.objects.filter(id=nid).delete()
    #重定向回部门列表
    return redirect('/user/list/')
