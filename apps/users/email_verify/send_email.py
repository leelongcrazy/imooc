#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
"""
    Time    : 2018/4/13 18:04
    Author  : LeeLong
    File    : send_email.py
    Software: PyCharm
    Description:
"""
from random import sample

from django.core.mail import send_mail

from users.models import EmailVerifyRecord


def generate_random_str(str_len=6):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(sample(list(chars), str_len))


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    # code = generate_random_str(12)
    code = '6699'
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = 'iMooc学习网注册链接'
        email_body = '请点击下面的链接可以激活你的帐号：https://www.imooc.org/active/{0}'.format(code)
        send_status = send_mail(email_title, email_body, from_email='', recipient_list=[email])
        if send_status:
            pass

    elif send_type == 'forget':
        email_title = 'iMooc学习网帐号找回链接'
        email_body = '请点击下面的链接可以找回密码：https://www.imooc.org/reset/{0}'.format(code)
        # send_status = send_mail(email_title, email_body, from_email='', recipient_list=[email])
        # if send_status:
        return
    elif send_type == 'email_update':
        email_title = 'iMooc学习网帐号邮箱修改验证码'
        email_body = '邮箱修改验证码为{0}'.format(code)


if __name__ == '__main__':
    f = generate_random_str(8)
    print(f)
