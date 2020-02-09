#!/usr/bin/env python
from random import Random  # 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
from web.models import EmailVerifyRecord  # 邮箱验证model
from django.conf import settings  # setting.py添加的的配置信息


# 生成随机字符串
def random_str(randomlength=6):
    """
    随机字符串
    :param randomlength: 字符串长度
    :return: String 类型字符串
    """
    str = ''
    chars = '0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 发送电子邮件
def send_code_email(email, send_type="register"):
    """
    发送电子邮件
    :param email: 要发送的邮箱
    :param send_type: 邮箱类型
    :return: True/False
    """
    code = random_str(6)
    email_record = EmailVerifyRecord.objects.create(code=code, email=email, send_type=send_type)

    # 如果为注册类型
    if send_type == "register":
        email_title = "注册激活"
        email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if not send_status:
            return False
    if send_type == "retrieve":
        email_title = "找回密码"
        email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if not send_status:
            return False
    return True
