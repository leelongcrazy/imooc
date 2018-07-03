#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
"""
    Time    : 2018/4/13 12:59
    Author  : LeeLong
    File    : forms.py
    Software: PyCharm
    Description:
"""
import re
from captcha.fields import CaptchaField
from django import forms


# 利用forms表单对用户输入的帐号信息进行初步验证，处理
from .models import UserInfo


class LoginForm(forms.Form):
    """
    用户登录表单
    """
    username = forms.CharField(required=True)  # 必填字段
    password = forms.CharField(required=True, min_length=6, max_length=20)  # 必填字段，最小长度为6，否则报错


class RegisterForm(forms.Form):
    """
    用户注册表单
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6, max_length=20)  # 必填字段，最小长度为6，否则报错
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ForgetForm(forms.Form):
    """
    用户忘记密码，验证码表单
    """
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ResetForm(forms.Form):
    """
    用户重置密码表单
    """
    password1 = forms.CharField(required=True, min_length=6, max_length=20)  # 必填字段，最小长度为6，否则报错
    password2 = forms.CharField(required=True, min_length=6, max_length=20)  # 必填字段，最小长度为6，否则报错


class UserImageForm(forms.ModelForm):
    """
    用户修改头像表单
    """
    class Meta:
        model = UserInfo
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    """
    用户修改个人信息表单
    """
    class Meta:
        model = UserInfo
        fields = ['nick_name', 'mobile', 'birth_day', 'address', 'gender']

    def clean_mobile(self):
        """
        用户填入手机号检查
        :return: mobile
        """
        mobile = self.cleaned_data['mobile']
        match = re.compile("^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\\d{8}$")
        if match.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("请输入正确的手机号码", code="mobile_invalid")


