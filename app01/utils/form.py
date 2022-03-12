from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError 
from django import forms
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5
class UserModelForm(BootStrapModelForm):
    class Meta:
        model=models.UserInfo
        fields=['name','password','age','account','create_time','gender','depart']
class PrettyModelForm(BootStrapModelForm):
    #mobile=forms.CharField(DISABLED=True,label='手机号') #不可点击
    #验证：方式一
    mobile=forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误')],
    )
    class Meta:
        model=models.PrettyNum
        fields=['mobile','price','level','status']
    #验证：方式二
    def clean_mobile(self):
        #获取当前编辑的id (self.instance.pk)
        txt_mobile=self.cleaned_data['mobile']        
        #手机号不能重复
        exists=models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()  #返回真假值
        if exists:
            raise ValidationError('手机号已存在')
        return txt_mobile
class AdminModelForm(BootStrapModelForm):
    confirm_password=forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True)
    )
    class Meta:
        model=models.Admin
        fields=['username','password','confirm_password']
        widgets={
            'password':forms.PasswordInput(render_value=True)
        }
    def clean_password(self):
        pwd=self.cleaned_data.get('password')
        return md5(pwd)
    def clean_confirm_password(self):
        print(self.cleaned_data)
        pwd=self.cleaned_data.get('password')
        confirm=md5(self.cleaned_data.get('confirm_password'))
        if pwd!=confirm:
            raise ValidationError('密码不一致！')
        #返回什么，字段以后保存到数据库就是什么
        return confirm
    #验证：方式二
    def clean_username(self):
        #获取当前编辑的id (self.instance.pk)
        txt_username=self.cleaned_data['username']        
        #手机号不能重复
        exists=models.Admin.objects.exclude(id=self.instance.pk).filter(username=txt_username).exists()  #返回真假值
        if exists:
            raise ValidationError('账号存在！')
        return txt_username
class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model=models.Admin
        fields=['username']
    #验证：方式二
    def clean_username(self):
        #获取当前编辑的id (self.instance.pk)
        txt_username=self.cleaned_data['username']        
        #手机号不能重复
        exists=models.Admin.objects.exclude(id=self.instance.pk).filter(username=txt_username).exists()  #返回真假值
        if exists:
            raise ValidationError('账号存在！')
        return txt_username
class AdminResetModelForm(BootStrapModelForm):
    confirm_password=forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True)
    )
    class Meta:
        model=models.Admin
        fields=['password','confirm_password']
        widgets={
            'password':forms.PasswordInput(render_value=True)
        }
    def clean_password(self):
        pwd=self.cleaned_data.get('password')
        md5_pwd=md5(pwd)
        #去数据库校验当前密码和新输入的密码是否一致
        exists=models.Admin.objects.filter(id=self.instance.pk,password=md5_pwd).exists()
        if exists:
            raise ValidationError('密码不能与以前的相同！')
        return md5_pwd
    def clean_confirm_password(self):
        print(self.cleaned_data)
        pwd=self.cleaned_data.get('password')
        confirm=md5(self.cleaned_data.get('confirm_password'))
        if pwd!=confirm:
            raise ValidationError('密码不一致！')
        #返回什么，字段以后保存到数据库就是什么
        return confirm