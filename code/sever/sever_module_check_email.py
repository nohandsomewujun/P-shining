#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/6/29 19:10
# @Author  : tzh
# @File    : sever_module_check_email.py
# @Software: PyCharm
import imapclient
import pyzmail
import pprint
import imaplib
import re

imap_type = ['mail.ustc.edu.cn',
             'imap.qq.com',
             'imap.163.com',
             ]
months = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'Apr', '06': 'Jun',
          '07': 'Jul', '08': 'Aug', '09': 'Sem', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
imaplib._MAXLINE = 100000


class EmailHandle:
    def __init__(self, account, password):
        self.UID_day = None
        self.msg = None
        self.raw_msg = None
        self.UID_unseen = None
        self.account = account
        self.password = password
        for imap in imap_type:
            if imap[5:] in account:
                break
        self.imapObj = imapclient.IMAPClient(imap, ssl=True)
        self.imapObj.login(account, password)
        self.imapObj.id_({"name": "IMAPClient", "version": "2.1.0"})

    def uid_unseen(self):
        self.imapObj.select_folder('INBOX', readonly=True)
        self.UID_unseen = self.imapObj.search('UNSEEN')
        num = len(self.UID_unseen)
        print("您有{}封未读邮件".format(num))
        return self.UID_unseen

    # 该方法返回一个包含未读邮件id信息的列表，索引越大发送时间越晚，可通过上述方法得到未读邮件数，在让用户决定是否需要查看未读邮件

    # 该方法用于获取某一条邮件的信息，返回的字典包含信息：
    """
    subject:邮件主题
    from：发送人和他的邮箱
    to：收件人（你）和邮箱
    text：邮件正文的文本部分
    html：邮件正文的html部分
    """

    def check_email(self, uid):
        email = {}
        self.imapObj.select_folder('INBOX', readonly=False)
        self.raw_msg = self.imapObj.fetch(uid, [b'BODY[]'])
        self.msg = pyzmail.PyzMessage.factory(self.raw_msg[uid][b'BODY[]'])
        email['subject'] = self.msg.get_subject()
        email['from'] = self.msg.get_addresses('from')  # 发件人及其邮箱
        email['to'] = self.msg.get_addresses('to')  # 收件人及其邮箱  这俩都是元组
        email['cc'] = self.msg.get_addresses('cc')  # 抄送情况，我觉得忽略,返回空列表，下同
        email['bcc'] = self.msg.get_addresses('bcc')  # 密件抄送字段，我觉得也可忽略
        if self.msg.text_part is not None:
            email['text'] = self.msg.text_part.get_payload().decode(self.msg.text_part.charset)
        else:
            email['text'] = None
        if self.msg.html_part is not None:
            email['html'] = self.msg.html_part.get_payload().decode(self.msg.html_part.charset)
        else:
            email['html'] = None
        return email

    # 该方法返回具体某一天的邮件id信息,date格式‘20220601’应是字符串
    def uid_day(self, date):
        date = corr_form(date)
        self.imapObj.select_folder('INBOX', readonly=True)
        self.UID_day = self.imapObj.search('ON ' + date)
        return self.UID_day

    def del_email(self, uid):
        self.imapObj.select_folder('INBOX', readonly=False)
        self.imapObj.delete_messages(uid)
        self.imapObj.expunge()

    def quit_link(self):
        self.imapObj.logout()

    # 返回尚未答复的邮件的id信息
    def uid_unanswered(self):
        self.imapObj.select_folder('INBOX', readonly=True)
        self.UID_day = self.imapObj.search('UNANSWERED')
        return self.UID_day


def corr_form(date):
    dateRegex = re.compile(r'(\d{4})(\d{2})(\d{2})')
    mo = dateRegex.search(date)
    month = months[mo.group(2)]
    date = mo.group(3) + '-' + month + '-' + mo.group(1)
    return date


def addr(num):
    if num == '1':
        return '@mail.ustc.edu.cn'   # 这里考虑到助教应该没有@ustc.edu.cn的邮箱后缀，就不分了
    elif num == '2':
        return '@qq.com'
    elif num == '3':
        return '@163.com'
    else:
        return 0  # 输入非1234就不要调用后续函数了


# 测试代码：
# num = input("邮箱后缀：")
# addr = addr(num)
# account = input("用户名") + addr
# password = input("密码")
# a = EmailHandle(account, password)
# uid = a.uid_unseen()
# print(uid)
# m = uid[0]
# print(a.check_email(m))
# print(a.uid_day('20220629'))
# a.quit_link()    # 最后记得与服务器断开连接

