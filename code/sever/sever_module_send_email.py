#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/6/28 21:18
# @Author  : tzh
# @File    : sever_module_send_email.py
# 文档说明：输入发送者的邮箱账号、密码、接收者的邮箱账号、发送人姓名，接收人姓名，邮件主题和正文内容
# send_account  发送者的邮箱账号
# send_password 发送者的密码
# receive_account   接收者的邮箱账号
# sender_name   发送人姓名
# receive_name  接收人姓名
# subject   邮件主题
# content   正文内容
import smtplib
# email 用于构建邮件内容
from email.mime.text import MIMEText
# 构建邮件头
from email.header import Header

# 备注：qq邮箱和网易邮箱需要先在设置中开启SMTP服务，先要向指定号码发送短信验证才能生成授权码，输入的是生成的16授权码而非密码,比较麻烦，
# @gmail.com连接总是超时，因此放弃
# 由于主流的邮箱就下面几种，为防止输入邮箱格式出错，做接口的时候可列出选项，这样用户直接输入用户名即可
smtp_type = [{'domain': 'mail.ustc.edu.cn', 'port': 465},
             {'domain': 'smtp.qq.com', 'port': 465},
             {'domain': 'smtp.163.com', 'port': 465},
             ]


def send_email(send_account, send_password, receive_account, sender_name, receiver_name, subject, content):
    for acc_type in smtp_type:
        if acc_type['domain'][5:] in send_account:
            break
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = Header(sender_name)  # 发送者
    msg['To'] = Header(receiver_name)  # 接收者
    msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题
    smtpObj = smtplib.SMTP_SSL(acc_type['domain'], acc_type['port'])
    smtpObj.ehlo()
    try:
        smtpObj.login(send_account, send_password)
    except smtplib.SMTPAuthenticationError:
        print("账号或密码输入错误")
    else:
        try:
            smtpObj.sendmail(send_account, receive_account, msg.as_string())
        except TimeoutError:
            print("由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。")
    finally:
        smtpObj.quit()


"""'1: @mail.ustc.edu.cn'
    '2: @qq.com'
    '3: @163.com'"""


def addr(num):
    if num == '1':
        return '@mail.ustc.edu.cn'   # 这里考虑到助教应该没有@ustc.edu.cn的邮箱后缀，就不分了
    elif num == '2':
        return '@qq.com'
    elif num == '3':
        return '@163.com'
    else:
        return 0  # 输入非1234就不要调用后续函数了


# 测试代码
# num = input("选择发送邮箱后缀")
# address = addr(num)
# send_account = input('用户名') + address
# send_password = input('密码')
# num = input("选择接收邮箱后缀")
# address = addr(num)
# receive_account = input('接收') + address
# sender_name = input('发送者姓名')
# receiver_name = input('接收者姓名')
# subject = input('主题')
# content = input('内容')
# send_email(send_account, send_password, receive_account, sender_name, receiver_name, subject, content)
