from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from blog.models import *
class Regform(forms.Form):
    whl=None
    # def __init__(self,request,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     self.request=request
    username=forms.CharField(
        min_length=3,
        max_length=12,
        error_messages={
            "min_length":"用户名长度过短",
            "max_length":"用户名长度过长",
            "required":"用户名不能为空"
        },
        widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"帐户名"})
    )
    password=forms.CharField(
        min_length=9,
        error_messages={
            "min_length":"密码长度过短",
            "required":"密码不能为空"
        },
        widget=widgets.PasswordInput(attrs={"class":"form-control","placeholder":"密码"})
    )
    repassword=forms.CharField(
        min_length=9,
        error_messages={
            "min_length":"密码长度过短",
            "required":"密码不能为空"
        },
        widget = widgets.PasswordInput(attrs={"class": "form-control","placeholder":"重新输入密码"})
    )
    email=forms.EmailField(
        error_messages={
            "required":"邮箱不能为空",
            "invalid":"邮箱格式错误"
        },
        widget=widgets.TextInput(attrs={"placeholder":"邮箱地址","class": "form-control"})
    )
    check_code=forms.CharField(
        error_messages={
            "required": "验证码不能为空",
        },
        widget=widgets.TextInput(attrs={"placeholder": "请输入右边图片中的验证码", "class": "form-control"})
    )
    # telphone=forms.IntegerField(
    #     max_value=11,
    #     min_value=11,
    #     error_messages={
    #         "required": "手机号不能为空",
    #         "invalid":"格式错误",
    #         "min_value":"手机号过短",
    #         "max_value":"手机号过长",
    #     },
    #     widget=widgets.TextInput(attrs={"placeholder": "手机号", "class": "form-control"})
    # )
    def clean_username(self):
        username = self.cleaned_data.get("username")
        user = UserInfo.objects.filter(username=username).first()
        if user:
            raise ValidationError("该用户已存在")
        else:
            return self.cleaned_data.get("username")
    def clean_password(self):
        if self.cleaned_data.get("password").isdigit():
            raise ValidationError("密码不能为纯数字")
        elif self.cleaned_data.get("password").isalpha():
            raise ValidationError("密码不能为纯字母")
        else:
            return self.cleaned_data.get("password")
    def clean_check_code(self):
        if self.cleaned_data.get("check_code").upper()==self.whl.upper():
            return self.cleaned_data.get("check_code")
        else:
            raise ValidationError("验证码输入不正确")
    def clean(self):
        if self.cleaned_data.get("password"):
            if self.cleaned_data.get("password") == self.cleaned_data.get("repassword"):
                return self.cleaned_data
            else:
                raise ValidationError("密码输入不一致")
        else:
            return self.cleaned_data

