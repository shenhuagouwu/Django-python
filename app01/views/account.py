from pyexpat import model
from django.shortcuts import render,redirect
from app01 import models
from django import forms

def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    #获取用户数据   
    username=request.POST.get('user')
    password=request.POST.get('pwd')
    queryset=models.Admin.objects.all()
    
    if username=='root' and password=='123':
        return HttpResponse('登陆成功')
    #return HttpResponse('登陆失败')
    return render(request,'login.html',{'error_msg':'登陆失败'})