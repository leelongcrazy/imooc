#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
"""
    Time    : 2018/4/14 18:19
    Author  : LeeLong
    File    : forms.py
    Software: PyCharm
    Description:基于model.Form来创建userAsk 的form表单
"""
import re
from django import forms
from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        自定义表单 mobile 字段验证方法
        :return:
        """
        mobile = self.cleaned_data['mobile']
        match = re.compile("^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\\d{8}$")
        if match.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("请输入正确的手机号码", code="mobile_invalid")

